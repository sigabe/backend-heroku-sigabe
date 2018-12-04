from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers, permissions
from sigabe.api import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="SIM API",
      default_version='v1',
   ),
   # validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

app_name = "api"


router = routers.DefaultRouter()
router.register('friends', views.FriendViewSet, basename='friend')
router.register('users', views.NonFriendViewSet, basename='user')
router.register('tracks', views.TrackSerializer, basename='track')
router.register('circles', views.CircleViewSet, basename='circle')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]
