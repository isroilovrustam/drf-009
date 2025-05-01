from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.serializers import ValidationError
from yaml import serialize

from shared.utiliy import send_email
from .serializers import SignUpSerializer, ChangeUserInformationSerializer, ChangeUserPhotoSerializer, LoginSerializer
from .models import User, NEW, CODE_VERIFIED, VIA_EMAIL, VIA_PHONE
from rest_framework import generics, permissions, status


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (permissions.AllowAny,)


class VerifyAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')  # 3789
        self.check_verify(user, code)
        return Response({
            'status': True,
            "auth_status": user.auth_status,
            "access": user.token()['access'],
            "refresh": user.token()['refresh_token'],
        })

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gt=timezone.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetnewVerificationAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.phone_number, code)
        else:
            data = {
                "message": "Email yoki nomeringiz xato"
            }
            raise ValidationError(data)
        return Response({
            'status': True,
            "message": "Tasdiqlash kodingiz qayta yuborildi"
        })

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=timezone.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message": "Kodingiz hali ishlatish uchun yaroqli, Kodni tekshirib qayta kiriting yoki bizor kuting"
            }

            raise ValidationError(data)


class ChangeUserInformationAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangeUserInformationSerializer
    http_method_names = ['patch', 'put']

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super(ChangeUserInformationAPIView, self).update(request, *args, **kwargs)
        data = {
            "success": True,
            "message": "Malumotlar qabul qilindi",
            "auth_status": self.request.user.auth_status,
        }
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        super(ChangeUserInformationAPIView, self).partial_update(request, *args, **kwargs)
        data = {
            "success": True,
            "message": "Malumotlar qabul qilindi",
            "auth_status": self.request.user.auth_status,
        }
        return Response(data, status=status.HTTP_200_OK)


class ChangeUserPhotoAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self,request, *args, **kwargs):
        serializer=ChangeUserPhotoSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            data = {
                "success": True,
                "message": "Malumotlar qabul qilindi rasm joylandi",
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer