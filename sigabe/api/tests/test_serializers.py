import pytest

from sigabe.api import serializers, models
from sigabe.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserSerializer:

    def test_user_detail(self):
        # create an object
        UserFactory()

        qs = models.User.objects.all()
        serializer = serializers.UserSerializer(
            qs,
            many=True
        )

        assert serializer.data
        assert len(serializer.data) == 1
        assert serializer.data[0]['id']
        assert serializer.data[0]['username']
        assert serializer.data[0]['name']


class TestFriendSerializer:

    def test_user_detail(self):
        # create an object
        UserFactory()

        qs = models.User.objects.all()
        serializer = serializers.FriendSerializer(
            qs,
            many=True
        )

        assert serializer.data
        assert len(serializer.data) == 1
        assert 'id' not in serializer.data[0]
        assert serializer.data[0]['username']
        assert serializer.data[0]['name']


class TestNonFriendSerializer:

    def test_user_detail(self):
        # create an object
        UserFactory()

        qs = models.User.objects.all()
        serializer = serializers.NonFriendSerializer(
            qs,
            many=True
        )

        assert serializer.data
        assert len(serializer.data) == 1
        assert 'id' not in serializer.data[0]
        assert serializer.data[0]['username']
        assert 'name' not in serializer.data[0]


class TestUserNameSerializer:

    def test_serde(self):
        # create an object
        UserFactory(username='jack')
        UserFactory(username='john')
        # models.User.objects.create(
        #     username='john'
        # )
        # models.User.objects.create(
        #     username='jack'
        # )

        qs = models.User.objects.all()
        assert qs.count() == 2
