from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from django.contrib.auth.models import User as AuthUser
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class SignupView(APIView):
  def post(self, request):
    data = request.data
    try:
      auth_user = AuthUser.objects.create_user(
        username = data['username'],
        email = data['email'],
        password = data['password']
      )
      
      user = User.objects.create(
        username=data['username'],
        email=data['email'],
        password=auth_user.password,
        role=data.get('role', 'user')
      )
      return Response({
        "message": "User created successfully",
      }, status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({
        "error": str(e)
      }, status=status.HTTP_400_BAD_REQUEST)
      
class LoginView(APIView):
  def post(self, request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    
    user = authenticate(username=username, password=password)
    if not user:
      return Response({
        "error": "Invalid credentials"
      }, status=status.HTTP_401_UNAUTHORIZED)
      
    try:
      custom_user = User.objects.get(email=user.email)
    except User.DoesNotExist:
      return Response({
        "error": "User not found"
      }, status=status.HTTP_404_NOT_FOUND)
      
    refresh = RefreshToken.for_user(user)
    
    access_token = refresh.access_token
    access_token["id"] = custom_user.id
    access_token["role"] = custom_user.role
    access_token["username"] = custom_user.username
    access_token["email"] = custom_user.email
    
    return Response({
      "message": "Login successful",
      "access_token": str(access_token),
    }, status=status.HTTP_200_OK)