import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from sigabe.users.tests.factories import UserFactory
from sigabe.users import models

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: settings.AUTH_USER_MODEL):
    assert user.get_absolute_url() == f"/users/{user.username}/"


def test_image():
    UserFactory()
    user = models.User.objects.first()

    # image = File(open('sigabe/static/images/test_image.jpeg').read)
    image = SimpleUploadedFile(
        name='test_image.jpeg',
        content=open('sigabe/static/images/test_image.jpeg', 'rb').read(),
        content_type='image/jpeg'
    )
    user.image = image
    user.save()

    user.refresh_from_db()
    assert user.image
