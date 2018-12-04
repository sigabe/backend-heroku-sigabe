from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, mixins
from rest_framework.decorators import action

from sigabe.api import models, serializers
from sigabe.api.permissions import WithinCicle

# Create your views here.


class FriendViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.FriendSerializer

    def get_queryset(self):
        qs = models.User.objects.filter(friends=self.request.user)
        return qs

    @action(methods=('delete',), detail=True, permission_classes=(permissions.IsAuthenticated,))
    def disconnect(self, request, pk=None):
        obj = self.get_object()
        user = self.request.user
        user.friends.remove(obj)

        return Response({'hello'}, status=status.HTTP_204_NO_CONTENT)


class NonFriendViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = serializers.NonFriendSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_fields = ('username',)

    def get_queryset(self):

        if self.request.user.is_authenticated:
            qs = models.User.objects.exclude(friends=self.request.user).exclude(pk=self.request.user.pk)
        else:
            qs = models.User.objects.all()

        return qs

    @action(methods=('post',), detail=True, permission_classes=(permissions.IsAuthenticated,))
    def connect(self, request, pk=None):
        obj = self.get_object()
        user = self.request.user
        user.friends.add(obj)

        return Response({}, status=status.HTTP_201_CREATED)


class TrackSerializer(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):

    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()

    def perform_create(self, serializer: serializers.LocationSerializer):
        serializer.save(user=self.request.user)


class CircleViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.CircleSerializer

    def get_queryset(self):
        return models.Circle.objects.filter(users=self.request.user)

    @action(methods=('post',), detail=True, permission_classes=(WithinCicle,))
    def connect(self, request, pk=None):
        obj = self.get_object()
        try:
            target = request.data['target']
            target = models.User.objects.get(pk=target)
        except (KeyError, ObjectDoesNotExist):
            return Response({'field': 'no target / invalid target'}, status=status.HTTP_400_BAD_REQUEST)

        obj.users.add(target)
        return Response({}, status=status.HTTP_201_CREATED)

    @action(methods=('delete',), detail=True, permission_classes=(WithinCicle,))
    def disconnect(self, request, pk=None):
        obj = self.get_object()
        try:
            target = request.data['target']
            target = models.User.objects.get(pk=target)
        except (KeyError, ObjectDoesNotExist):
            return Response({'field': 'no target / invalid target'}, status=status.HTTP_400_BAD_REQUEST)

        if target not in obj.users.all():
            return Response({'field': 'target not in circle'}, status=status.HTTP_400_BAD_REQUEST)

        obj.users.remove(target)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
