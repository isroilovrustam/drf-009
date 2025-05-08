from django.urls import path
from .views import CreateUserAPIView, VerifyAPIView, GetnewVerificationAPIView, ChangeUserInformationAPIView, \
    ChangeUserPhotoAPIView, LoginView, LogOutView, LoginRefreshView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path("signup/", CreateUserAPIView.as_view(), name="signup"),
    path("verify/", VerifyAPIView.as_view(), name="verify"),
    path("new-verify/", GetnewVerificationAPIView.as_view(), name="new-verify"),
    path("change-user/", ChangeUserInformationAPIView.as_view(), name="change-user"),
    path("change-user-photo/", ChangeUserPhotoAPIView.as_view(), name="change-user-photo"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path('login-refresh/', LoginRefreshView.as_view(), name="login-refresh"),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot-password"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset-password"),
]
