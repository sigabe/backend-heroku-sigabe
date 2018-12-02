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

        # check whether the data given
        # is complete or not
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

        # check whether the data given
        # is partial ( not exposing all user's data)
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

        # check whether the data given
        # is protecting most of user's data
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

        qs = models.User.objects.all()

        assert qs.count() == 2

        user, target = qs

        serializer = serializers.ConnectionSerializer(
            data={'username': target.username}
        )

        # check the ability to add friends
        # and still maintaining privacy
        # of the user

        assert serializer.is_valid()

        serializer.save(user=user)
        user.refresh_from_db()

        assert target in user.friends.all()
        assert 'id' not in serializer.data
        assert 'name' not in serializer.data
        assert serializer.data['username']

    def test_unrecognized_username(self):
        proto_user = UserFactory.build()

        serializer = serializers.ConnectionSerializer(
            data={'username': proto_user.username}
        )

        assert not serializer.is_valid()
