from django.urls import path
from . import views


urlpatterns = [
    path('login-register/',views.loginpage, name = 'login-register'),
    path('logout/',views.logoutUser, name = 'logout'),
    path('register/',views.registerpage, name = 'register'),
    
    path('',views.home, name = 'home'),
    path('room/<str:pk>/',views.room, name = 'room'),
    path('profile/<str:pk>/',views.profilep, name = 'profile'),
    
    path('create-room/',views.createRoom, name = 'create-room'),
    path('update-room/<str:pk>/',views.updateRoom, name = 'update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom, name = 'delete-room'),
    path('delete-message/<str:pk>/',views.deletemessage, name = 'delete-message'),
    path('update_user/',views.updateUser, name = 'update_user'),
    path('topc/',views.topc, name = 'topc'),
]

