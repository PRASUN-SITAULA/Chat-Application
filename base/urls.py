from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('user_register/', views.registerUser, name="user_register"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('login/', views.LoginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('delete-Message/<str:pk>/', views.deleteMessage, name="delete-Message"),
    path('delete-Messages/<str:pk>/', views.deleteMessages, name="delete-Messages"),
    path('profile/<str:pk>/', views.UserProfile, name="UserProfile"),
    path('update-user/', views.UpdateUser, name="update-user"),
    path('topics/', views.TopicsPage, name="TopicsPage"),
    path('activity/', views.ActivityPage, name="activity"),

]
