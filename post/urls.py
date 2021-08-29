from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [

	path('', post_home, name='posts-home'),
	path('likes-unlike/', like_unlike_post, name='like-unlike'),
	path('<pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
	path('<pk>/update/', PostUpdateView.as_view(), name="post-update"),

	
]