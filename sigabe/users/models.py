from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ImageField, UUIDField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from sigabe.users.helpers import RandomFileName
import uuid


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    id = UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    image = ImageField(null=True, upload_to=RandomFileName('users/image'))

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
