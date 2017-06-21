from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Client(models.Model):
    creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    birth_Day = models.DateField(blank=False, null=False)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True, default="photos/no_foto.png", verbose_name='')
    likes = models.IntegerField(verbose_name='Нравится', default=0)

    @property
    def age(self):
        return models.DateField.auto_now - self.birth_Day

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey('auth.User')
    text = models.TextField(verbose_name='Комментарий')
    time = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.time = timezone.now()
        self.save()
