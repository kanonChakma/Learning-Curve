from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import NewUser, Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host", "participants"]


class UserForm(ModelForm):
    class Meta:
        model = NewUser
        fields = ["avatar", "name", "username", "email", "bio"]


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = NewUser
        fields = ["name", "username", "email", "password1", "password2"]
