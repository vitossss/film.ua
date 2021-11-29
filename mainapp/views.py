from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.base import View

from .models import *
from django.views.generic import ListView, DetailView
from .forms import *


class GenreYear:
    def get_genres(self):
        return Genre.objects.all().order_by('name')

    def get_years(self):
        return Movie.objects.values('year').filter(draft=False).order_by('year')[:4]


class MovieList(GenreYear, ListView):
    """Список фільмів"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetail(GenreYear, DetailView):
    """Один фільм"""
    model = Movie
    slug_field = 'url'


class FilterMovies(GenreYear, ListView):
    def get_queryset(self):
        if all([self.request.GET.getlist('year'), self.request.GET.getlist('genre')]):
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist('year')) &
                Q(genres__in=self.request.GET.getlist('genre'))
            ).distinct()
        elif self.request.GET.getlist('year'):
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist('year'))
            ).distinct()
        elif self.request.GET.getlist('genre'):
            queryset = Movie.objects.filter(
                Q(genres__in=self.request.GET.getlist('genre'))
            ).distinct()
        return queryset


class Search(ListView):
    """Пошук фільмів"""
    template_name = 'mainapp/search.html'

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'{self.request.GET.get("q")}&'
        return context


class AddReview(View):
    """Додавання відгуку"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())
