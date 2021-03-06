import pytest


from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from sigabe.api import serializers, views, models
from sigabe.api.tests import factories
from sigabe.users.tests.factories import UserFactory

import uuid


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
        response = client_resource.delete(f'/api/friends/{user_resource[1].id}/connections/')

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

    @pytest.mark.django_db(transaction=True)
    def test_connect(self, client_resource, user_resource):
        user_resource[0].friends.remove(user_resource[1])
        user_resource[0].save()

        response = client_resource.post(f'/api/users/{user_resource[1].pk}/connections/')

        assert response.status_code == status.HTTP_201_CREATED

        user_resource[0].refresh_from_db()
        assert user_resource[1] in user_resource[0].friends.all()


class TestTrackViewSet:

    def test_track(self, client_resource, user_resource):
        proto_location = factories.LocationFactory.build()
        response = client_resource.post('/api/tracks/', {
            'longitude': proto_location.longitude,
            'latitude': proto_location.latitude
        })

        assert response.status_code == status.HTTP_201_CREATED

        user_resource[0].refresh_from_db()
        assert user_resource[0].locations.exists()


class TestCircleViewSet:

    def test_create(self, client_resource, user_resource):
        proto_circle = factories.CircleFactory.build()
        response = client_resource.post('/api/circles/', {
            'name': proto_circle.name,
            'image': proto_circle.image
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_list(self, client_resource, user_resource):
        circle = factories.CircleFactory()
        location = factories.LocationFactory()

        circle.users.add(user_resource[0])
        circle.users.add(location.user)
        circle.save()

        response = client_resource.get(f'/api/circles/{circle.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['users']) == 2

    def test_connect_valid_target(self, client_resource, user_resource):
        circle = factories.CircleFactory()
        circle.users.add(user_resource[0])

        response = client_resource.post(f'/api/circles/{circle.pk}/connections/', {
            'target': user_resource[0].pk
        })

        circle.refresh_from_db()

        assert response.status_code == status.HTTP_201_CREATED
        assert user_resource[0] in circle.users.all()

    def test_disconnect_valid_target(self, client_resource, user_resource):
        circle = factories.CircleFactory()
        circle.users.add(user_resource[0])

        response = client_resource.delete(f'/api/circles/{circle.pk}/connections/', {
            'target': user_resource[0].pk
        })

        circle.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user_resource[0] not in circle.users.all()

    def test_connect_invalid_target(self, client_resource, user_resource):
        circle = factories.CircleFactory()
        circle.users.add(user_resource[0])

        response = client_resource.post(f'/api/circles/{circle.pk}/connections/', {
            'target': uuid.uuid4()
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_disconnect_nonexistent_target(self, client_resource, user_resource):
        circle = factories.CircleFactory()
        circle.users.add(user_resource[0])

        response = client_resource.delete(f'/api/circles/{circle.pk}/connections/', {
            'target': uuid.uuid4()
        })

        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_disconnect_invalid_target(self, client_resource, user_resource):
        circle = factories.CircleFactory()
        circle.users.add(user_resource[0])

        response = client_resource.delete(f'/api/circles/{circle.pk}/connections/', {
            'target': user_resource[1].pk
        })

        print(response.data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
