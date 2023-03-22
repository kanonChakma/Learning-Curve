from django.contrib import admin
from django.urls import include, path

from .views import (
    activityPage,
    createRoom,
    deleteMessage,
    deleteRoom,
    home,
    loginPage,
    logutUser,
    regitsterPage,
    room,
    topicsPage,
    updateRoom,
    updateUser,
    userProfile,
)

urlpatterns = [
    path("", home, name="home"),
    path("room/<int:pk>/", room, name="room"),
    path("create-room/", createRoom, name="create-room"),
    path("update-room/<str:pk>", updateRoom, name="update-room"),
    path("user-profile/<str:pk>", userProfile, name="user-profile"),
    path("delete-room/<str:pk>", deleteRoom, name="delete-room"),
    path("login/>", loginPage, name="login"),
    path("logout/>", logutUser, name="logout"),
    path("register/>", regitsterPage, name="register"),
    path("delete-message/<int:pk>/", deleteMessage, name="delete-message"),
    path("update-user/", updateUser, name="update-user"),
    path("topics/", topicsPage, name="topics"),
    path("activity/", topicsPage, name="activity"),
]
