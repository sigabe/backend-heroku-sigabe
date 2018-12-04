import pytest

from sigabe.api import serializers
from sigabe.api.tests import factories

pytestmark = pytest.mark.django_db


class TestLocationSerializer:

    def test_validity(self):
        proto_location = factories.LocationFactory.build()

        serializer = serializers.LocationSerializer(
            data={
                'user': proto_location.user,
                'longitude': proto_location.longitude,
                'latitude': proto_location.latitude
            }
        )

        assert serializer.is_valid()


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
