from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def loginPage(request):
   page = 'login'
   # if user is already logged in
   if request.user.is_authenticated :
      return redirect('home')
   
   if request.method == 'POST':
      # retrieve data from the input from form
      username = request.POST.get('username').lower()
      password = request.POST.get('password')
      # check if username exist on the database
      try:
         user = User.objects.get(username=username)
      except:
         messages.error(request, ' User does not exist')
         return redirect('loginPage')
      # authenticate if password and username matches
      user = authenticate(request, username=username, password=password)
      #checks if a valid user is retrieved
      if user is not None:
         login(request, user)
         messages.success(request, 'Login successful!')
         return redirect('home')
      else:
         messages.error(request, ' Invalid username or password')
   context = {'page': page}
   return render(request, 'login_register.html', context)


def logoutUser(request):
   logout(request)
   return redirect('home')

def registerPage(request):
   form = UserCreationForm()

   if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.username = user.username.lower()
         user.save()
         login(request, user)
         return redirect('home')
      else:
          messages.error(request, ' Something went wrong!')
   context = {'form': form}
   return render(request,'login_register.html', context )


def home(request):
  #it gets the value of q (inputted sa search bar) then if present, store sa q, else , store empty string
  q = request.GET.get('q') if request.GET.get('q') != None else ''

   #shown rooms are filtered by conditions.
   #retrieve a list of objects from the database that match the specified conditions.
   #Q object = used to build complex queries using the OR operator
   #topic__name__ = foreign keys
   # icontains is a case-insensitive containment check.
   # name__icontains=q  ==  checks if nag match ba ang naa sa q variable
  rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
  
  topics = Topic.objects.all()
#   messages = Message.objects.all()
  context = {'rooms': rooms, 'topics': topics}
  return render(request, 'home.html', context)


def room(request, pk):
    rooms = Room.objects.get(id=pk)
    context = {'rooms': rooms}
    return render(request, 'room.html', context)


@login_required(login_url='loginPage')
def createRoom(request):
   #to show the form
   form = RoomForm()

  #handling the data - sending to the database
   if request.method == 'POST':
      form = RoomForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('home')
      
   context = {'form': form}
   return render(request, 'createRoom.html', context)

@login_required(login_url='loginPage')
def updateRoom(request, pk):
   #access the data from database
   room = Room.objects.get(id=pk)
   #like a placeholder, pre inputted form -data from database
   form = RoomForm(instance=room)
   #restricting other users to update other room
   if request.user != room.host:
      return HttpResponse('You are not allowed here!')
   
   #saving data to databse
   if request.method == 'POST':
      form = RoomForm(request.POST, instance=room)
      if form.is_valid():
         form.save()
         return redirect('home')
   context={'form': form}
   return render(request, 'updateRoom.html', context)

@login_required(login_url='loginPage')
def deleteRoom(request, pk):
   room = Room.objects.get(id=pk)
   #restricting other users to delete other room
   if request.user != room.host:
      return HttpResponse('You are not allowed here!')
   if request.method == 'POST':
      room.delete()
      return redirect('home')
   context={'obj':room}
   return render(request, 'deleteRoom.html', context)