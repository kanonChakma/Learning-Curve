from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import MyUserCreationForm, RoomForm, UserForm
from .models import Message, NewUser, Room, Topic


def userProfile(request, pk):
    user = NewUser.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    activites = user.message_set.all()

    context = {
        "topics": topics,
        "rooms": rooms,
        "room_messages": activites,
        "user": user,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    room_id = message.room.id
    print(message.user, room_id, request.user)
    if request.user != message.user:
        return HttpResponse("You are not to allowed delete")

    if request.method == "POST":
        message.delete()
        return redirect("room", pk=room_id)
    return render(request, "base/delete.html", {"obj": message})


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        try:
            user = NewUser.objects.get(email=email)
        except:
            messages.error(request, "user does not exist!!")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "username or password does not exist!!")
    context = {"page": page}
    return render(request, "base/login.html", context)


def regitsterPage(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Error Occured During Registration!!")
    return render(request, "base/register.html", {"page": "register", "form": form})


def logutUser(request):
    page = "logout"
    logout(request)
    return redirect("home")


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )

    activity = Message.objects.filter(Q(room__topic__name__icontains=q))
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        "rooms": rooms,
        "topics": topics,
        "rooms_count": rooms_count,
        "room_messages": activity,
    }
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()  # many to one relationships here
    print(room_messages)
    participants = room.participants.all()  # many to  many relationship here

    if request.method == "POST":
        messge = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        # if participants.count(request.user) == 0:
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     form = form.save(commit=False)
        #     form.host = request.user
        #     form.save()
        #     return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)  # form will be prefilled with room value
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("Your are not allowed here!!")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get("name")
        room.description = request.POST.get("description")
        room.topic = topic
        room.save()
        return redirect("home")

        # form = RoomForm(
        #     request.POST, instance=room
        # )  # identify which room value will update/replace
        # if form.is_valid():
        #     form.save()
        #     return redirect("home")
    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("Your are not allowed here!!")

    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "base/delete.html", {"obj": room})


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        form.save()
        return redirect("user-profile", pk=user.id)
    return render(request, "base/update-user.html", {"form": form})

    # user = request.user
    # form = UserForm(instance=user)

    # if request.method == 'POST':
    #     form = UserForm(request.POST, request.FILES, instance=user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user-profile', pk=user.id)


def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, "base/topics.html", {"topics": topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", {"room_messages": room_messages})
