from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterUserForm
from .models import Note
from .serializers import NoteSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"message": "This is a protected view"})


class NoteListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(View):
    template_name = "register_user.html"
    form_class = RegisterUserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
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


class HomeView(ListView):
    model = Note
    template_name = "home.html"
    context_object_name = "object_list"

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
