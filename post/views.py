from django.shortcuts import render, redirect
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm, ReplyModelForm
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from itertools import chain
# Create your views here.

@login_required
def post_home(request):
	profile = Profile.objects.get(user = request.user)
	user = [user for user in profile.friends.all()]
	posts = []
	qs = None
	for u in user:
		p = Profile.objects.get(user = u)
		post = p.get_posts()
		
		posts.append(post)

	my_posts = profile.get_posts()
	
	posts.append(my_posts)

	print("posts", posts)

	no = False

	if len(posts) > 0:
		qs = sorted(chain(*posts), reverse=True, key = lambda obj: obj.created)
		

	if len(qs) == 0:
		no = True

	print(len(qs))
	

	p_form = PostModelForm()
	c_form = CommentModelForm()
	r_form = ReplyModelForm()
	post_added = False


	if 'submit_p_form' in request.POST:
		print(request.POST)
		p_form = PostModelForm(request.POST, request.FILES)
		if p_form.is_valid():
			instance = p_form.save(commit = False)
			instance.author = profile
			instance.save()
			p_form = PostModelForm()
			post_added = True

	if 'submit_c_form' in request.POST:
		c_form = CommentModelForm(request.POST)
		if c_form.is_valid():
			instance = c_form.save(commit = False)
			instance.user = profile
			instance.post = Post.objects.get(id = request.POST.get('post_id'))
			instance.save()
			c_form = CommentModelForm()

	context = {
	'qs' : qs,
	'profile': profile,
	'p_form': p_form,
	'c_form':c_form,
	'r_form': r_form,
	'post_added': post_added,
	'no_posts': no
	}
	return render(request, 'posts/main.html', context)

@login_required
def like_unlike_post(request):
	user = request.user
	if request.method == 'POST':
		post_id = request.POST.get('post_id')
		profile = Profile.objects.get(user = request.user)
		post_obj = Post.objects.get(id = post_id)

		if profile in post_obj.liked.all():
			post_obj.liked.remove(profile)

		else:
			post_obj.liked.add(profile)

		like, created = Like.objects.get_or_create(user = profile, post_id = post_id)

		if not created:
			if like.value == 'Like':
				like.value = 'Unlike'
			else:
				like.value = 'Like'
		else:
			like.value = 'Like'

		data = {

		'value':like.value,
		'count':post_obj.liked.all().count()

		}

		return JsonResponse(data, safe=False)

		like.save()
		post_obj.save()
	return redirect('posts:posts-home')


class PostDeleteView(LoginRequiredMixin, DeleteView):
	model = Post
	template_name = 'posts/confirm_del.html'
	success_url = reverse_lazy('posts:posts-home')

	def get_obj(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		obj = Post.objects.get(pk = pk)

		if not obj.author.user == self.request.user:
			messages.warning(self.request, "You cant' delete this!")

		return obj

class PostUpdateView(LoginRequiredMixin, UpdateView):
	model = Post
	form_class = PostModelForm
	success_url = reverse_lazy('posts:posts-home')
	template_name = 'posts/update.html'




