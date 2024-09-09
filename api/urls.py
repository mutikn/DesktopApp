from django.urls import path, include
from api.views import RegisterView, UsersView, CommentApiView
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'get_active_users', UsersView, basename='active-users')
router.register(r'comments', CommentApiView, basename='get-comment')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
]   