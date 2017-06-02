from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.TextField()
    surname = models.TextField()

    def __str__(self):
        return self.Name
