from .models import Profile, Relationship

def profile_pic(request):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
		picture = profile.avtar
		return {'picture': picture}
	return {}

def get_counter(request):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user = request.user)
		count = Relationship.objects.get_invitation(profile).count()
		return {'count': count}
	return {}
