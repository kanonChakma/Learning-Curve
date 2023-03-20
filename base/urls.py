from django.contrib import admin
from django.urls import include, path

from .views import createRoom, deleteRoom, home, room, updateRoom

urlpatterns = [
    path("", home, name="home"),
    path("room/<int:pk>", room, name="room"),
    path("create-room/", createRoom, name="create-room"),
    path("update-room/<int:pk>", updateRoom, name="update-room"),
    path("delete-room/<int:pk>", deleteRoom, name="delete-room"),
]
