from rest_framework import serializers 

from application.models import User, Comment

from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email','id')


class CommentSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['creator'] = request.user
        return super().create(validated_data)
    
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'creator', 'created')
        read_only_fields = ('creator',)