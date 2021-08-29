from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):

	user = request.user
	print(type(user))

	print(user)
	if request.user.is_anonymous:
		no_login = True
	else:
		no_login = False

	print(no_login)
	

	context = {
	'user' : user,
	'no_login' : no_login
	
	}

	return render(request, 'main/home.html', context)
	#return HttpResponse("Hey World")