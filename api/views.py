from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from application.models import User
from application.serializers import  RegisterSerializer, UsersSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "STATUS": status.HTTP_201_CREATED,
        }, status=status.HTTP_201_CREATED)


class UsersView(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed"}, status=405)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed"}, status=405)

    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed"}, status=405)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed"}, status=405)
