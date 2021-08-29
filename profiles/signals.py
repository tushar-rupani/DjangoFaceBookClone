from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from .models import Profile, Relationship

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user = instance)

@receiver(post_save, sender = Relationship)
def post_save_add_friends(sender, instance, created, **kwargs):
	sender_ = instance.sender
	receiver_ = instance.receiver

	if instance.status == 'received':
		sender_.friends.add(receiver_.user)
		receiver_.friends.add(sender_.user)

		sender_.save()
		receiver_.save()
		
	elif instance.status == 'block':
		sender_.friends.remove(receiver_.user)
		receiver_.friends.remove(sender_.user)
		sender_.save()
		receiver_.save()


@receiver(pre_delete, sender=Relationship)
def pre_delete_relation(sender, instance, **kwargs):
	sender = instance.sender
	receiver = instance.receiver

	receiver.friends.remove(sender.user)
	sender.friends.remove(receiver.user)

	sender.save()
	receiver.save()