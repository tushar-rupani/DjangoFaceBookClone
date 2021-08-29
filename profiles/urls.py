from django.urls import path
from .views import *


app_name = 'profiles'

urlpatterns = [

	path('', ProfileListView.as_view(), name='all_profiles_list'),
	path('followers/<pk>/', my_followers, name='followers'),
	path('my-profile/', my_profile, name='my-profile'),
	path('requests/', get_invitation, name='requests'),
	path('invite_profiles/', invite_profile_list_view, name='invite_profiles'),
	path('send-invite/', send_invitation, name='send-invite'),
	path('block-user/', block_user, name='block-user'),
	path('block-friends/', blocked_friends, name='block-friends'),
	path('unblock-user/', unblock_user, name='unblock-user'),
	path('remove-friend/', remove_friend, name='remove-friend'),
	path('requests/accept-request', accept_invite, name="accept-invite"),
	path('requests/reject-request', reject_invite, name="reject-invite"),
	path('search/', search, name="search"),
	path('<slug>/', ProfileDetailView.as_view(), name='profile-detail-view'),

	
	
]