from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatApp, name='chatApp'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),  
]
