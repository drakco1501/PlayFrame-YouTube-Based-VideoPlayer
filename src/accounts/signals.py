from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import * 


@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email,
        )
    else:
        profile, _ = Profile.objects.get_or_create(user=instance)
        profile.username = instance.username
        profile.email = instance.email
        profile.save()

@receiver(post_save, sender=Profile)
def update_user_fields_from_profile(sender, instance, **kwargs):
    user = instance.user

    updated = False

    # Update username if different
    if user.username != instance.username:
        user.username = instance.username
        updated = True

    # Update email if different
    if user.email != instance.email:
        user.email = instance.email
        updated = True

    if updated:
        user.save()
