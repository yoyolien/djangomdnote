# urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import (
    HomeView,
    RegisterUserView,
    NoteListCreateView,
    LoginUserView,
    ProtectedView,
)

urlpatterns = [
    path("", NoteListCreateView.as_view()),
    path("home", HomeView.as_view()),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("verifytest", ProtectedView.as_view()),
]
