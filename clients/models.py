from django.db import models


class Client(models.Model):
    Name = models.TextField()
    Surname = models.TextField()
    age = models.IntegerField()

    def __str__(self):
        return self.Name
