from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from application.models import User, Comment
from application.serializers import  RegisterSerializer, UsersSerializer, CommentSerializer


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


class CommentApiView(ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def perform_create(self, serializer):

        serializer.save()


    def update(self, request, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, id=pk)

        if comment.creator.id == request.user.id:
            serializer = self.get_serializer(comment, data = request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return Response({"detail": "Comment has been updated"}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None, *args, **kwargs):
        comment = get_object_or_404(Comment, id=pk)

        if comment.creator.id == request.user.id:
            comment.delete()
            return Response({"detail": "Comment has been deleted"}, status=status.HTTP_200_OK)
        
        return Response({"detail": "You do not permission to delete"}, status=status.HTTP_403_FORBIDDEN)