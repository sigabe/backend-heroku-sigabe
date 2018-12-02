from typing import Dict, Any

from sigabe.api import models
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.User
        fields = ('id', 'username', 'name', 'email', 'image')


class FriendSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.User
        fields = ('username', 'name', 'email', 'image')


class NonFriendSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.User
        fields = ('username', 'image')


class ConnectionSerializer(serializers.HyperlinkedModelSerializer):

    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ('username', 'image')
        read_only_fields = ('image',)

    def validate_username(self, value: str):
        if not models.User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'username not found'
            )

        return value

    def create(self, validated_data: Dict[str, Any]):
        user = validated_data['user']
        target = models.User.objects.get(username=validated_data['username'])
        user.friends.add(target)
        user.save()

        return target
