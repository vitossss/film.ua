from django import forms
from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    video = forms.CharField(label='Трейлер', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


admin.site.register(Category)
admin.site.register(Genre)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm


admin.site.register(MoviesShots)
admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(RatingStar)
admin.site.register(Reviews)
