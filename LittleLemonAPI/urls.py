from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test),
    path('groups/manager/users', views.managers),
]