from django.urls import path
from .views import CreateUserAPIView, VerifyAPIView, GetnewVerificationAPIView, ChangeUserInformationAPIView

urlpatterns = [
    path("signup/", CreateUserAPIView.as_view(), name="signup" ),
    path("verify/", VerifyAPIView.as_view(), name="verify" ),
    path("new-verify/", GetnewVerificationAPIView.as_view(), name="new-verify" ),
    path("change-user/", ChangeUserInformationAPIView.as_view(), name="change-user" ),
]
