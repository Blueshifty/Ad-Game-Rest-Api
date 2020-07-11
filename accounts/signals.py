from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import User


@receiver(pre_save, sender=User)
def delete_file_on_change_extension(sender, instance, **kwargs):
    if instance.id:
        try:
            old_avatar = User.objects.get(id=instance.id).avatar
        except User.DoesNotExist:
            return
        else:
            if old_avatar:
                old_avatar.delete(save=False)
