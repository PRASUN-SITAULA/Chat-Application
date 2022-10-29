from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm,  MyUserCreationForm
from django.db.models import Q

# Create your views here.


def LoginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User doesnot exist.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesnot exist.')

    context = {'page':page}
    return render(request, 'base/user_login.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')



def registerUser(request):
    
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Error!! Please try again.')
    return render(request, 'base/user_login.html', {'form': form})



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rooms = Room.objects.filter(Q(topic__name__icontains=q)| Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
 
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    return render(request, 'base/home.html',{'rooms': rooms,'topics':topics, 'room_count':room_count, 'room_messages':room_messages})

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method =="POST":
        messages = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')

        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room':room, 'room_messages':room_messages, 'participants':participants,}
    return render(request,'base/room.html',context)
 
def UserProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context  = {'user': user, 'rooms': rooms, 'room_messages':room_messages,'topics':topics}
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')

def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        #form = RoomForm(request.POST)
        #if form.is_valid():
           #room.host = request.user
            #room.save()
        return redirect(home)

    context = {'form':form}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are not the user.")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        return redirect('home')
    context = {'form': form, 'topics':topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):

    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not the user.")

    
    if request.method == "POST":
        room.delete()
        return redirect(home)
    return render(request, 'base/delete.html', {'obj': room})





@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not the user.")

    
    if request.method == "POST":
        message.delete()
        return redirect(home)
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def deleteMessages(request,pk):
    messages = Message.objects.get(id=pk)

    if request.user != messages.user:
        return HttpResponse("You are not the user.")

    
    if request.method == "POST":
        messages.delete()
        return redirect(home)
    return render(request, 'base/delete.html', {'obj':messages})


@login_required(login_url='login')
def UpdateUser(request):
    user = request.user
    form = MyUserCreationForm(instance=user)

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('UserProfile', pk=user.id)
    return render(request, 'base/update-user.html', {'form': form})



def TopicsPage(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics':topics})   

def ActivityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages':room_messages})