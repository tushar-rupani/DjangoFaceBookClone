from django.urls import path
from .views import *

app_name = 'chat'

urlpatterns = [

	path('', chat_home, name='chat-home'),
	path('checkview', checkview, name='checkview'),
	path('send', send, name='send'),
	path('getMessages/<str:room>/', getMessages, name="getMessages"),
	path('delete/<int:room>', delete, name="delete"),
	path('<str:room>/', room, name='room'),
	
	

	
]