from django.shortcuts import render
from rest_framework import generics, status,permissions
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
User = get_user_model()


def success_response(message, data=None, status_code=200):
    response = {
        "success": True,
        "statusCode": status_code,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return Response(response, status=status_code)


def error_response(message, error_details=None, status_code=400):
    response = {
        "success": False,
        "message": message,
    }
    if error_details is not None:
        response["errorDetails"] = error_details
    return Response(response, status=status_code)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        response = super().create(request)
        return success_response("User registered successfully",  status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Invalid Credential.", serializer.errors)

        username_or_email = serializer.validated_data['username']
        password = serializer.validated_data['password']
        # user = self.perform_authentication(username_or_email, password)

        user = User.objects.filter(username=username_or_email).first(
        ) or User.objects.filter(email=username_or_email).first()
        if user:
            user = authenticate(
                request, username=user.username, password=password)
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return success_response("User logged in successfully", {
                    # "user": UserSerializer(user).data,
                    # "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
            return error_response("Invalid Credential.", "Password is incorrect", status.HTTP_400_BAD_REQUEST)
        return error_response("Invalid username or email.", "User not found", status.HTTP_400_BAD_REQUEST)





class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_object(self):
        return self.request.user  
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
