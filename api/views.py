from rest_framework.viewsets import ModelViewSet

from application.models import User
from application.serializers import UserSerializer


class UserApiView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

