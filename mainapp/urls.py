from django.urls import path

from .views import *

urlpatterns = [
    path('movies/', MovieList.as_view(), name='movie_list'),
    path('movies/filter/', FilterMovies.as_view(), name='filter'),
    path('movies/<slug:slug>/', MovieDetail.as_view(), name='movie_detail'),
    path('search/', Search.as_view(), name='search'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
]
