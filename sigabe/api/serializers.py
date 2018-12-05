from typing import Dict, Any

from sigabe.api import models
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'username', 'name', 'email', 'image')


class FriendSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.User
        fields = ('url', 'username', 'name', 'email', 'image')
        extra_kwargs = {
            'url': {'view_name': 'api:user-detail'}
        }


class InCircleFriendSerializer(serializers.HyperlinkedModelSerializer):

    location = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('username', 'name', 'image', 'location')

    def get_location(self, instance: models.User):
        location = instance.locations.all().order_by('-datetime').first()

        if not location:
            return

        longitude, latitude = location.longitude, location.latitude
        return {'longitude': longitude, 'latitude': latitude}


class NonFriendSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.User
        fields = ('url', 'username', 'image')
        extra_kwargs = {
            'url': {'view_name': 'api:user-detail'}
        }


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Location
        # fields = '__all__'
        exclude = ('url',)
        read_only_fields = ('user',)
        extra_kwargs = {
            'user': {'view_name': 'api:user-detail'}
        }


class CircleSerializer(serializers.HyperlinkedModelSerializer):

    users = InCircleFriendSerializer(many=True, read_only=True)

    class Meta:
        model = models.Circle
        fields = '__all__'
        read_only_fields = ('creator',)
        extra_kwargs = {
            'url': {'view_name': 'api:circle-detail'},
        }

    def create(self, validated_data):
        user = validated_data.pop('user')
        instance = super().create(validated_data)
        instance.users.add(user)
        instance.save()
        return instance
