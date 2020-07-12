from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserUpdateSerializer
from .models import User


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User Registration Successful',
        }
        return Response(response, status=status_code)


class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User logged in successfully',
            'refresh': serializer.data['refresh'],
            'access': serializer.data['access']
        }

        return Response(response, status=status_code)


class UserUpdateView(CreateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class AuthTest(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK, data={
            'user_id': request.user.id,
            'user_name': request.user.user_name,
            'name': request.user.first_name + " " + request.user.last_name,
        })
