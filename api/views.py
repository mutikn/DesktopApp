from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from application.models import User
from application.serializers import  RegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "STATUS": status.HTTP_201_CREATED,
        }, status=status.HTTP_201_CREATED)

