from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer
from .utils import send_activation_email


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_activation_email(user)
            return Response('Аккаунт успешно создан.', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(get_user_model(), activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response(
            'Ваш аккаунт успешно активирован.',
            status=status.HTTP_200_OK
        )


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response(
            'Вы успешно вышли из своего аккаунта.'
        )