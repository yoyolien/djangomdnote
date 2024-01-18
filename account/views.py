from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

from .forms import RegisterUserForm


# Create your views here.
class RegisterUserView(View):
    template_name = "register_user.html"
    form_class = RegisterUserForm

    def get(self, request: HttpRequest):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, "home.html")
        else:
            return render(request, self.template_name, {"form": form})


class LoginUserView(LoginView):
    template_name = "login.html"
    LOGIN_REDIRECT_URL = "home"
    def form_valid(self, form):
        response = super().form_valid(form)

        access_token = str(RefreshToken.for_user(self.request.user))

        response.set_cookie(key='access_token', value=access_token, httponly=True)
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response


class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)  # 從header中獲取token

        if header is None:
            # 如果header中沒有令牌，嘗試從cookie中獲取
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)  # 從header中獲取原始token
        if raw_token is None:
            return None  # 如果沒有token，返回None

        validated_token = self.get_validated_token(raw_token)  # 驗證token
        return self.get_user(validated_token), validated_token  # 返回用戶和驗證過的token
