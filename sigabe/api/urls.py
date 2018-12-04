from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from sigabe.api import views

app_name = "api"


router = routers.DefaultRouter()
router.register('friends', views.FriendViewSet, basename='friend')
router.register('users', views.NonFriendViewSet, basename='user')
router.register('tracks', views.TrackSerializer, basename='track')
router.register('circles', views.CircleViewSet, basename='circle')

urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]
