from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import ListView
from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Note
from .serializers import NoteSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"message": "This is a protected view"})


class NoteListCreateView(APIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        responses={200: NoteSerializer(many=True)}
    )
    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=NoteSerializer)
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@login_required()
class HomeView(ListView):
    model = Note
    template_name = "home.html"
    context_object_name = "object_list"

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
