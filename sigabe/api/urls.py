from django.urls import path, include
from django.conf.urls import url

app_name = "api"
urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]
