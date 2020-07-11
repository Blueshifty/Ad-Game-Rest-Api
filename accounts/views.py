from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import UserLoginSerializer, UserRegistrationSerializer


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
