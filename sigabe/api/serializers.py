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
        fields = ('username', 'name', 'image')

    def get_location(self, instance: models.User):
        location = instance.locations.all().order_by('-date').first()
        longitude, latitude = location.longitude, location.latitude
        return {'longitude': longitude, 'latitude': latitude}


class NonFriendSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.User
        fields = ('url', 'username', 'image')


# class ConnectionSerializer(serializers.HyperlinkedModelSerializer):

#     username = serializers.CharField()

#     class Meta:
#         model = models.User
#         fields = ('username', 'image')
#         read_only_fields = ('image',)

#     def validate_username(self, value: str):
#         if not models.User.objects.filter(username=value).exists():
#             raise serializers.ValidationError(
#                 'username not found'
#             )

#         return value

#     def create(self, validated_data: Dict[str, Any]):
#         user = validated_data['user']
#         target = models.User.objects.get(username=validated_data['username'])
#         user.friends.add(target)
#         user.save()

#         return target


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Location
        fields = '__all__'
        read_only_fields = ('user',)


class CircleSerializer(serializers.HyperlinkedModelSerializer):

    users = InCircleFriendSerializer(many=True, read_only=True)

    class Meta:
        model = models.Circle
        fields = '__all__'
        read_only_fields = ('creator',)
