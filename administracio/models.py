from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


from bases.models import ClasseBase
#from idlelib.iomenu import blank_re
       
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserExt( ClasseBase):
    #user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to=user_directory_path)
    
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserExt.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userext.save()
    
    
