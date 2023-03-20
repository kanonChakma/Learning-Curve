from django.contrib import admin

from .models import Message, Room, Topic

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Topic)


# class RoomAdmin(admin.ModelAdmin):
#     fields = ["id", "host", "topic", "name", "description", "updated", "created"]


# class TopicAdmin(admin.ModelAdmin):
#     fields = ["id", "name"]


# class MeassgeAdmin(admin.ModelAdmin):
#     fields = ["id", "user", "room", "body", "updated", "created"]
