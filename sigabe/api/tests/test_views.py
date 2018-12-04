import pytest


from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from sigabe.api import serializers, views, models
from sigabe.api.tests import factories
from sigabe.users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


@pytest.fixture()
def user_resource():
    john = UserFactory(username='john')
    jack = UserFactory(username='jack')

    john.friends.add(jack)
    john.save()

    john.refresh_from_db()
    jack.refresh_from_db()
    yield john, jack


@pytest.fixture()
def client_resource(user_resource):
    client = APIClient()
    token = Token.objects.create(user=user_resource[0])
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


class TestFriendViewSet:

    def test_anonymous_protection(self, user_resource):
        client = APIClient()
        response = client.get('/api/friends/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db(transaction=True)
    def test_list(self, client_resource, user_resource):
        response = client_resource.get('/api/friends/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['username'] == user_resource[1].username

    @pytest.mark.django_db(transaction=True)
    def test_unfriend(self, client_resource, user_resource):
        response = client_resource.delete(f'/api/friends/{user_resource[1].id}/disconnect/')

        assert response.status_code == status.HTTP_200_OK

        user_resource[0].refresh_from_db()
        assert not user_resource[0].friends.exists()


class TestNonFriendViewSet:

    def test_anonymous_availability(self):
        user = UserFactory()
        client = APIClient()

        response = client.get('/api/users/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['username'] == user.username

    @pytest.mark.django_db(transaction=True)
    def test_nonfriend_availability(self, client_resource, user_resource):
        user_resource[0].friends.remove(user_resource[1])
        user_resource[0].save()

        response = client_resource.get('/api/users/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['username'] == user_resource[1].username

    def test_nonfriend_unavailability(self, client_resource, user_resource):
        response = client_resource.get('/api/users/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0


class TestCircleFactorySerializer:

    def test_validity(self):
        proto_circle = factories.CircleFactory.build()

        serializer = serializers.CircleSerializer(
            data={
                'name': proto_circle.name,
                'image': proto_circle.image,
            }
        )

        assert serializer.is_valid()
