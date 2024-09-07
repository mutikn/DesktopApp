from django.urls import path, include
from api.views import UserApiView

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', UserApiView)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]