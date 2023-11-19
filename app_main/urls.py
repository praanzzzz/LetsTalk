from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('loginPage', views.loginPage, name='loginPage'),
    path('registerPage', views.registerPage, name='registerPage'),
    path('logoutUSer', views.logoutUser, name='logoutUser'),
    path('room/<str:pk>/', views.room, name='room'),
    path('createRoom', views.createRoom, name='createRoom'),
    path('updateRoom/<str:pk>', views.updateRoom, name='updateRoom'),
    path('deleteRoom/<str:pk>/', views.deleteRoom, name='deleteRoom')
]