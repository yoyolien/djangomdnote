# urls.py
from django.urls import path, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import (
    HomeView,
    NoteListCreateView,
    ProtectedView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="API documentation for My App",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", NoteListCreateView.as_view()),
    path("home", HomeView.as_view(),name="home"),
    path("verifytest", ProtectedView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
