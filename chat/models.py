from django.db import models

# Create your models here.

class Room(models.Model):
	name = models.CharField(max_length = 200)

	def __str__(self):
		return str(self.name)

class Message(models.Model):
	value = models.CharField(max_length = 1000)
	room = models.CharField(max_length = 200)
	user = models.CharField(max_length = 100)
	date = models.DateTimeField(auto_now_add = True)

	
