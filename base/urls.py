from django.contrib import admin
from django.urls import include, path

from .views import (
    createRoom,
    deleteMessage,
    deleteRoom,
    home,
    loginPage,
    logutUser,
    regitsterPage,
    room,
    updateRoom,
)

urlpatterns = [
    path("", home, name="home"),
    path("room/<str:pk>", room, name="room"),
    path("create-room/", createRoom, name="create-room"),
    path("update-room/<str:pk>", updateRoom, name="update-room"),
    path("delete-room/<str:pk>", deleteRoom, name="delete-room"),
    path("login/>", loginPage, name="login"),
    path("logout/>", logutUser, name="logout"),
    path("register/>", regitsterPage, name="register"),
    path("delete-message/<int:pk>/", deleteMessage, name="delete-message"),
]
