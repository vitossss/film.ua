from datetime import date
from django.urls import reverse
from django.db import models


class Category(models.Model):
    """Категорія"""
    name = models.CharField('Категорія', max_length=100)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Actor(models.Model):
    """Актори і режисери"""
    name = models.CharField('Ім\'я', max_length=100)
    age = models.PositiveIntegerField('Вік', default=0)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='actors/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Актори і режисери'
        verbose_name_plural = 'Актори і режисери'


class Genre(models.Model):
    """Жанри"""
    name = models.CharField('Ім\'я', max_length=100)
    description = models.TextField('Опис')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Movie(models.Model):
    """Фільми"""
    title = models.CharField('Назва', max_length=100)
    tagline = models.CharField('Слоган', max_length=100, default='')
    description = models.TextField('Опис')
    video = models.TextField('Трейлер', blank=True, null=True)
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveIntegerField('Дата релізу', default=2019)
    country = models.CharField('Країна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='режисер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='актори', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='жанри')
    world_premiere = models.DateField('Прем\'єра у світі', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='вказати суму в долларах')
    fees_in_usa = models.PositiveIntegerField('Збори в Америці', default=0, help_text='вказати суму в долларах')
    fees_in_world = models.PositiveIntegerField('Збори у світі', default=0, help_text='вказати суму в долларах')
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=100, unique=True)
    draft = models.BooleanField('Чорновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фільм'
        verbose_name_plural = 'Фільми'


class MoviesShots(models.Model):
    """Кадри з фільма"""
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='movies_shots')
    movie = models.ForeignKey(Movie, verbose_name='Фільм', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр з фільма'
        verbose_name_plural = 'Кадри з фільма'


class RatingStar(models.Model):
    """Рейтинг"""
    value = models.PositiveIntegerField('Значення', default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Зірка рейтингу'
        verbose_name_plural = 'Зірки рейтингу'


class Rating(models.Model):
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, verbose_name='зірка', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='фільм', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.star, self.movie)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    """Відгуки"""
    email = models.EmailField()
    name = models.CharField('Ім\'я', max_length=100)
    text = models.TextField('Повідомлення', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Батько', on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, verbose_name='фільм', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.name, self.movie)

    class Meta:
        verbose_name = 'Відгук'
        verbose_name_plural = 'Відгуки'
