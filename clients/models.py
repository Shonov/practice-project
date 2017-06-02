from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.TextField(max_length=50)
    surname = models.TextField(max_length=50)
    birthDay = models.DateField()
    photo = models.ImageField(upload_to="photos/")
    creator = models.ForeignKey('auth.User')

    @property
    def age(self):
        return models.DateField.auto_now - self.birthDay

    def __str__(self):
        return self.name
