from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.db.models import Q

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm

from .models import Room,Topic,Message
from .forms import RoomForm,UserForm


def loginpage(request):
    page ='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method =="POST":
        username =request.POST.get('username').lower()
        password =request.POST.get('password')
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'user does not exist:')
        user = authenticate(request,username = username,password=password)
        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, 'username or password does not exist:')
            
    context = {'page': page}
    return render(request,'news/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')
def registerpage(request):
    form = UserCreationForm()
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'error occured during registration:')
    context = {'form':form}
    return render(request,'news/login_register.html',context)
            

def home(request):
    q = request.GET.get('q')if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains =q)|
        Q(name__icontains =q) |
        Q(discription__icontains =q)
    )
    topics = Topic.objects.all()[0:2]
    room_count = rooms.count()
    r_messages = Message.objects.filter(Q(room__topic__name__icontains =q))
    
    
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'r_messages':r_messages}
    return render(request,'news/home.html',context)
def room(request, pk):
    room = Room.objects.get(id=pk)
    r_messages = room.message_set.order_by('-created').all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'r_messages': r_messages,'participants':participants}
    return render(request, 'news/room.html', context)

def profilep(request,pk):
    user = User.objects.get(id =pk)
    rooms = user.room_set.all()
    r_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'r_messages':r_messages,'topics':topics}
    return render(request,'news/profile.html',context)
    

@login_required(login_url="login-register")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room = Room.objects.create(
            host = request.user,
            topic = topic,
            name =request.POST.get('name'),
            discription =request.POST.get('discription')
        )
    # this is using form
    #     form =RoomForm(request.POST)
    #     if form.is_valid():
    #         room =form.save(commit=False)
    #         room.host = request.user
    #         room.save()
    # 
        return redirect('home')    
    context = {'form':form, 'topics':topics }
    return render(request,'news/room_form.html',context)
@login_required(login_url="login-register")
def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user!=room.host:
        return HttpResponse("you are not allowed here")
        
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name =request.POST.get('name'),
        room.topic = topic,
        room.discription =request.POST.get('discription')
        room.save()
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
            
    context ={'form':form, 'topics':topics, 'room':room }
    return render(request,'news/room_form.html',context)
@login_required(login_url="login-register")
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)
    if request.user!=room.host:
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context ={'obj':room}
    return render(request,'news/delete.html',context)
@login_required(login_url="login-register")
def deletemessage(request,pk):
    message = Message.objects.get(id = pk)
    if request.user!=message.user:
        return HttpResponse("you are not allowed here")
    if request.method == 'POST':
        message.delete()
        return redirect('room')
    context ={'obj':message}
    return render(request,'news/delete.html',context)
@login_required(login_url="login-register")            
def updateUser(request):
    user = request.user
    userf = UserForm(instance=user)
    if request.method == "POST":
        userf = UserForm(request.POST,instance=user)
        if userf.is_valid:
           userf.save()
           return redirect('profile', pk=user.id)
    context ={'userf':userf} 
    return render(request, 'news/update_user.html',context)

def topc(request):
    q = request.GET.get('q')if request.GET.get('q')!=None else ''
    topics = Topic.objects.filter(name__icontains =q)
    context ={'topics':topics}
    return render(request, 'news/topics.html', context)