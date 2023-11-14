from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm

# Create your views here.


def home(request):
  rooms = Room.objects.all()
  topics = Topic.objects.all()
  messages = Message.objects.all()
  context = {'rooms': rooms, 'topics': topics, 'messages':messages}
  return render(request, 'home.html', context)


def room(request, pk):
    rooms = Room.objects.get(id=pk)
    context = {'rooms': rooms}
    return render(request, 'room.html', context)

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

def updateRoom(request, pk):
   #access the data from database
   room = Room.objects.get(id=pk)
   #like a placeholder, pre inputted form -data from database
   form = RoomForm(instance=room)
   #saving data to databse
   if request.method == 'POST':
      form = RoomForm(request.POST, instance=room)
      if form.is_valid():
         form.save()
         return redirect('home')
   context={'form': form}
   return render(request, 'updateRoom.html', context)

def deleteRoom(request, pk):
   room = Room.objects.get(id=pk)
   if request.method == 'POST':
      room.delete()
      return redirect('home')
   context={'obj':room}
   return render(request, 'deleteRoom.html', context)