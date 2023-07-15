from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Teacher


@receiver(sender=User, signal=post_save)
def create_teacher(sender, instance, created, **kwargs):
    if created:
        teacher = Teacher.objects.create(
            user=instance,
            fullname=f'{instance.first_name} {instance.last_name}'.title(),
            first_name=instance.first_name,
            last_name=instance.last_name,
        )
        teacher.save()


@receiver(sender=Teacher, signal=post_save)
def change_credentials(sender, instance, created, **kwargs):
    if not created:
        user = instance.user
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.save()


@receiver(sender=Teacher, signal=post_delete)
def user_delete_on_teacher_deleted(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
