from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Room, Message
from profiles.models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def chat_home(request):
	context = {
	'user': request.user
	}
	return render(request, 'chat/home.html')

@login_required
def room(request, room):
	room_details = Room.objects.get(name = room)
	print(room)
	print(room_details)

	username = request.GET['username']
	print(username)
	context = {
	'room': room,
	'username': username,
	'room_details': room_details
	}
	return render(request, 'chat/room.html', context )

@login_required
def send(request):
	username = request.POST['username'] 
	room_id = request.POST['room_id'] 
	message = request.POST['message'] 

	new_mes = Message.objects.create(room = room_id, value = message, user = username)
	new_mes.save()
	return HttpResponse("Message Sent")

@login_required
def getMessages(request, room):
	room = Room.objects.get(name = room)
	message = Message.objects.filter(room = room.id)
	return JsonResponse({'messages':list(message.values())})

@login_required
def delete(request, room):
	message = Message.objects.filter(room = room).delete()
	return redirect('chat:chat-home')


@login_required
def checkview(request):
	username = request.POST.get('username')
	room = request.POST.get('room_name')

	if Room.objects.filter(name = room).exists():
		return redirect('/chat/' + room + '/?username=' + username)

	else:
		new_room = Room.objects.create(name = room)
		new_room.save()
		return redirect('/chat/' + room + '/?username=' + username)

