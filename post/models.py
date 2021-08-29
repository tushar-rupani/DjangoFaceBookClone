from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.

class Post(models.Model):
	content = models.TextField()
	image = models.ImageField(blank=True, validators = [FileExtensionValidator(['jpg', 'png', 'jpeg'])], upload_to='posts/')
	liked = models.ManyToManyField(Profile, blank=True, related_name="likes")
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(Profile, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.content[:20])

	def get_likes_no(self):
		return self.liked.all().count()

	def get_comments_no(self):
		return self.comment_set.all().count()

	class Meta:
		ordering = ('-created',)


LIKES = (

	('Like', 'Like'),
	('Unlike', 'Unlike')

	)

class Like(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	value = models.CharField(choices = LIKES, max_length=10)

	def __str__(self):
		return f"{self.user}-{self.post}-{self.value}"


class Comment(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	body = models.TextField(max_length=100)

	def __str__(self):
		return f"{self.user}-{self.body}"

class Reply(models.Model):
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	body = models.CharField(max_length = 200)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	

	def __str__(self):
		return str(self.body)

    
    
    	


    
    	



