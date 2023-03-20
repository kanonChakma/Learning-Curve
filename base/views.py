from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import RoomForm
from .models import Room, Topic


def home(request):
    q = request.GET.get("q")

    if q is not None:
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q)|
            Q(name__icontains=q)|
            Q(description__icontains=q)
            )
    else:
        rooms = Room.objects.all()

    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = {"rooms": rooms, "topics": topics,"rooms_count":rooms_count}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "base/room.html", context)


def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})
