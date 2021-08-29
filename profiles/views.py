from django.shortcuts import render, redirect
from .models import *
from .forms import ProfileFormClass
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def my_profile(request):
	obj = Profile.objects.get(user = request.user)
	form = ProfileFormClass(request.POST or None, request.FILES or None, instance = obj)
	confirm = False

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			confirm = True

	context = {
	'obj' : obj,
	'form' : form,
	'confirm' : confirm
	}

	return render(request , 'profiles/my_profile.html', context)

@login_required
def get_invitation(request):
	profile = Profile.objects.get(user = request.user)
	obj = Relationship.objects.get_invitation(profile)
	print(obj)
	results = list(map(lambda x: x.sender, obj))
	print(results)

	is_empty = False
	if len(results) == 0:
		is_empty = True

	context = {
	'obj' : results,
	'is_empty': is_empty,
	'profile': profile
	}

	return render(request, 'profiles/invitation.html', context)

@login_required
def profile_list_view(request):
	user = request.user
	obj = Profile.objects.get_all_profiles(user)

	context = {
	'obj' : obj
	}

	return render(request, 'profiles/profile_list.html', context)

@login_required
def invite_profile_list_view(request):
	user = request.user
	obj = Profile.objects.get_all_profiles_to_invite(user)

	context = {
	'obj' : obj
	}

	return render(request, 'profiles/invite_profile_list.html', context)



class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        blocked = profile.blocked_users.all()
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        context["blocked"] = blocked
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

@login_required
def send_invitation(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		print(pk)
		user = request.user
		sender = Profile.objects.get(user = user)
		receiver = Profile.objects.get(pk = pk)

		rel = Relationship.objects.create(sender = sender, receiver = receiver, status = 'send')

		return redirect(request.META.get('HTTP_REFERER'))

	return redirect('profiles:my-profile')

@login_required
def blocked_friends(request):
	profile = Profile.objects.get(user = request.user)
	blocked = profile.blocked_users.all()
	block_list = []
	for block in blocked:
		block_profiles = Profile.objects.get(user = block)
		block_list.append(block_profiles)

	print(block_list)
	count = blocked.count()
	context = {
	'blocked' : blocked,
	'count': count,
	'list': block_list
	}
	return render(request, 'profiles/blocked_users.html', context)

@login_required
def unblock_user(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		unblock_profile = Profile.objects.get(pk = pk)
		myprof = Profile.objects.get(user = request.user)
		myprof.blocked_users.remove(unblock_profile.user)
		myprof.save()
		return redirect(request.META.get('HTTP_REFERER'))
	return redirect('profiles:my-profile')


@login_required
def block_user(request):

		if request.method == 'POST':
			pk = request.POST.get('profile_pk')
			block_profile = Profile.objects.get(pk = pk)
			myprof = Profile.objects.get(user = request.user)
			myprof.blocked_users.add(block_profile.user)
			myprof.save()
			block_profile.friends.remove(myprof.user)
			myprof.friends.remove(block_profile.user)
			block_profile.save()
			myprof.save()
			print("Done")
			try:
				rel = Relationship.objects.get(

				(Q(sender = block_profile) & Q(receiver = myprof)) | (Q(sender = myprof) & Q(receiver = block_profile))

				)
				print("relation",rel)
				rel.delete()

			except:
				pass
			
			return redirect(request.META.get('HTTP_REFERER'))

		return redirect('profiles:my-profile')



@login_required
def remove_friend(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		user = request.user
		sender = Profile.objects.get(user = user)
		receiver = Profile.objects.get(pk = pk)

		rel = Relationship.objects.get(

			(Q(sender = sender) & Q(receiver = receiver)) | (Q(sender = receiver) & Q(receiver = sender))

			)
		rel.delete()
		return redirect(request.META.get('HTTP_REFERER'))
	return redirect('profiles:my-profile')

@login_required
def accept_invite(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		print(pk)
		sender = Profile.objects.get(pk = pk)
		receiver = Profile.objects.get(user = request.user)
		rel = Relationship.objects.get(sender = sender, receiver = receiver)

		if rel.status == 'send':
			rel.status = 'received'
			rel.save()
	return redirect('profiles:requests')

@login_required
def reject_invite(request):
	if request.method == 'POST':
		pk = request.POST.get('profile_pk')
		print(pk)
		sender = Profile.objects.get(pk = pk)
		receiver = Profile.objects.get(user = request.user)
		rel = Relationship.objects.get(sender = sender, receiver = receiver)
		rel.delete()
	return redirect('profiles:requests')

class ProfileDetailView(LoginRequiredMixin, DetailView):
	model = Profile
	template_name = 'profiles/detail.html'

	def get_object(self, slug = None):
		slug = self.kwargs.get('slug')
		profile = Profile.objects.get(slug = slug)
		return profile

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		slug = self.kwargs.get('slug')

		user = User.objects.get(username__iexact=self.request.user)
		profile = Profile.objects.get(user = user)
		blocked = profile.blocked_users.all()
		print("block users", blocked) 

		if profile.slug == slug:
			myprof = True
		else:
			myprof = False

		print("myprof", myprof)

		rel_r = Relationship.objects.filter(sender = profile)

		rel_s = Relationship.objects.filter(receiver = profile)

		

		rel_sender = []

		rel_receiver = []

		for item in rel_r:
			rel_receiver.append(item.receiver.user)

		for item in rel_s:
			rel_sender.append(item.sender.user)

		context["rel_receiver"] = rel_receiver
		context["rel_sender"] = rel_sender
		context["myprof"] = myprof
		context["blocked"] = blocked
		context['posts'] = self.get_object().get_posts()
		context['length'] = True if len(self.get_object().get_posts()) > 0 else False
		return context


def search(request):
	
	query = request.GET['q']
	print(query)
	profile = Profile.objects.get(user = request.user)
	all_profiles = Profile.objects.filter(user__username__icontains = query)
	rel_r = Relationship.objects.filter(sender = profile)
	rel_s = Relationship.objects.filter(receiver = profile)
	rel_sender = []
	rel_receiver = []
	for item in rel_r:
		rel_receiver.append(item.receiver.user)

	for item in rel_s:
		rel_sender.append(item.sender.user)




	context = {
	'all_profiles':all_profiles,
	'rel_receiver':rel_receiver,
	'rel_sender':rel_sender
	}

	return render(request, 'profiles/search.html', context)

def my_followers(request, pk):
	profile = Profile.objects.get(pk = pk)
	obj = profile.get_friends()
	print(obj)

	friend_list = []

	for qs in obj:
		friends = Profile.objects.get(user = qs)
		friend_list.append(friends)
		print(friend_list)


	profile = Profile.objects.get(user = request.user)

	
	
	rel_r = Relationship.objects.filter(sender = profile)
	rel_s = Relationship.objects.filter(receiver = profile)
	rel_sender = []
	rel_receiver = []
	for item in rel_r:
		rel_receiver.append(item.receiver.user)

	for item in rel_s:
		rel_sender.append(item.sender.user)

	context = {
	'profile':profile,
	'obj' : friend_list,
	'rel_receiver':rel_receiver,
	'rel_sender':rel_sender
	}
	return render(request, 'profiles/followers.html', context)






