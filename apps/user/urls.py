from django.urls import path
from .views import CreateUserAPIView, VerifyAPIView, GetnewVerificationAPIView, ChangeUserInformationAPIView, \
    ChangeUserPhotoAPIView, LoginView, LogOutView, LoginRefreshView

urlpatterns = [
    path("signup/", CreateUserAPIView.as_view(), name="signup"),
    path("verify/", VerifyAPIView.as_view(), name="verify"),
    path("new-verify/", GetnewVerificationAPIView.as_view(), name="new-verify"),
    path("change-user/", ChangeUserInformationAPIView.as_view(), name="change-user"),
    path("change-user-photo/", ChangeUserPhotoAPIView.as_view(), name="change-user-photo"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path('login-refresh/', LoginRefreshView.as_view(), name="login-refresh"),
]
