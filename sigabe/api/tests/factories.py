from typing import Any, Sequence

import factory
from factory import DjangoModelFactory, Faker, post_generation
from django.core.files.uploadedfile import SimpleUploadedFile
from sigabe.users.tests.factories import UserFactory
from sigabe.api import models
import random


class LocationFactory(DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    longitude = random.random()
    latitude = random.random()

    class Meta:
        model = models.Location
        django_get_or_create = ['user', 'longitude', 'latitude']


class CircleFactory(DjangoModelFactory):

    name = Faker('name')
    image = SimpleUploadedFile(
        name='test_image.jpeg',
        content=open('sigabe/static/images/test_image.jpeg', 'rb').read(),
        content_type='image/jpeg'
    )

    class Meta:
        model = models.Circle
        django_get_or_create = ['name']
