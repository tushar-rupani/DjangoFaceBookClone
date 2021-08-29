from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.shortcuts import reverse


class ProfileManager(models.Manager):
	def get_all_profiles(self, me):
		obj = Profile.objects.all().exclude(user = me)
		return obj

	def get_all_profiles_to_invite(self, sender):
		profiles = Profile.objects.all().exclude(user = sender)
		profile = Profile.objects.get(user = sender)

		qs = Relationship.objects.filter(Q(sender = profile) | Q(receiver = profile))

		accepted = set([])

		for rel in qs:
			if rel.status == 'received':
				accepted.add(rel.receiver)
				accepted.add(rel.sender)

		available = [profile for profile in profiles if profile not in accepted]

		return available


class Profile(models.Model):
	first_name = models.CharField(max_length = 200, blank=True)
	last_name = models.CharField(max_length = 200, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length = 300, default="No Bio..")
	email = models.EmailField()
	coutry = models.CharField(max_length = 200, blank=True)
	avtar = models.ImageField(default = 'avtar/avtar.jpg', upload_to='avtar/')
	friends = models.ManyToManyField(User, blank=True, related_name='friends')
	blocked_users = models.ManyToManyField(User, blank=True, related_name='blocked_users')

	slug = models.SlugField(unique = True, blank=True)

	updated = models.DateTimeField(auto_now = True)
	created = models.DateTimeField(auto_now_add = True)

	objects = ProfileManager()

	def get_absolute_url(self):
		return reverse("profiles:profile-detail-view", kwargs={"slug":self.slug})


	def __str__(self):
		return f"{self.user.username}"

	def get_friend_no(self):
		return self.friends.all().count()

	def get_friends(self):
		return self.friends.all()

	def get_posts_no(self):
		print(self.post_set.all())
		return self.post_set.all().count()

	def get_posts(self):
		return self.post_set.all()

	def get_likes_given_no(self):
		likes = self.like_set.all()
		total_liked = 0
		for item in likes:
			if item.value == "Like":
				total_liked += 1
		return total_liked

		

	def likes_received(self):
		posts = self.post_set.all()
		total_liked = 0

		for item in posts:
			total_liked += item.liked.all().count()
		return total_liked

	__initial_first_name = None
	__initial_last_name = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__initial_first_name = self.first_name
		self.__initial_last_name = self.last_name



	def save(self, *args, **kwargs):
		ex = False
		to_slug = self.slug
		if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or self.slug=="":
			if self.first_name and self.last_name:
				to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
				ex = Profile.objects.filter(slug = to_slug).exists()
			else:
				to_slug = self.user.username
			while ex:
				to_slug = slugify(to_slug + " " + get_random_code())
				ex = Profile.objects.filter(slug = to_slug).exists()
		else:
			to_slug = str(self.user)


		self.slug = to_slug
		super().save(*args, **kwargs)

CHOICES = (

	('send', 'send'),
	('received', 'received'),
	('block', 'block')

)


class RelationshipManager(models.Manager):
	def get_invitation(self, receiver):
		obj = Relationship.objects.filter(status = 'send', receiver=receiver)
		return obj

class Relationship(models.Model):
	sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
	receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
	status = models.CharField(max_length = 10, choices = CHOICES)
	updated = models.DateTimeField(auto_now = True)
	created = models.DateTimeField(auto_now_add = True)

	objects = RelationshipManager()

	def __str__(self):
		return str(self.sender)

