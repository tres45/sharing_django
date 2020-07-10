from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import date
import os


try:
    user = User.objects.create_user(
        username=os.environ.get('DJANGO_LOGIN'),
        password=os.environ.get('DJANGO_PASS'),
        is_staff=True, is_superuser=True
    )
    user.save()
except Exception:
    pass


class Category(models.Model):
    """Categories"""
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Guide(models.Model):
    """Guides and managers"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Информация")
    image = models.ImageField("Фотография", upload_to="guides/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("guide_detail", kwargs={"slug": self.name})

    class Meta:
        verbose_name = "Гид и менеджер"
        verbose_name_plural = "Гиды и менеджеры"


class Hike(models.Model):
    """Hikes"""
    title = models.CharField("Название похода", max_length=100)
    tagline = models.TextField("Слоган", default="")
    description = models.TextField("Описание")
    image = models.ImageField("Фотография", upload_to="hikes/")
    country = models.CharField("Страна", max_length=50)
    region = models.CharField("Регион", max_length=50)
    start_date = models.DateField("Начало похода", default=date.today)
    finish_date = models.DateField("Окончание похода", default=date.today)
    duration = models.PositiveIntegerField("Продолжительность", default=0, help_text="in days")
    price = models.PositiveIntegerField("Стоимость", default=0, help_text="Цена в грн")
    guide = models.ManyToManyField(Guide, verbose_name="Гид", related_name="hike_guide")
    manager = models.ManyToManyField(Guide, verbose_name="Менеджер", related_name="hike_manager")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("hike_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Поход"
        verbose_name_plural = "Походы"


class HikePhotos(models.Model):
    """Photos from hike"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Фотография", upload_to="hike_photos/")
    hike = models.ForeignKey(Hike, verbose_name="Поход", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фотография с похода"
        verbose_name_plural = "Фотографии с похода"


class Reviews(models.Model):
    """Reviews for hike"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Отзыв", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    hike = models.ForeignKey(Hike, verbose_name="поход", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.hike}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
