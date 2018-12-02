from django.db import models
from sigabe.users.models import User
from sigabe.users.helpers import RandomFileName

import uuid

# Create your models here.


class Location(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, related_name='locations', on_delete=models.CASCADE)
    langitude = models.FloatField()
    latitude = models.FloatField()
    datetime = models.DateTimeField(auto_now_add=True)


class Circle(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    creator = models.ForeignKey(User, related_name='own_circles', on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=RandomFileName('circles/image'))
    users = models.ManyToManyField(User, related_name='circles')
