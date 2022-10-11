from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """model proxy to users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    git = models.URLField(blank=True)
    image = models.ImageField(upload_to='users/pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username


# signals to create profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     full_name = models.CharField('Nombres', max_length=100)
#     date_birth = models.DateField(
#         'Fecha de nacimiento', 
#         blank=True,
#         null=True
#     )
#     #
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'

#     REQUIRED_FIELDS = ['full_name']

#     objects = UserManager()

#     def get_email(self):
#         return self.email
    
#     def get_full_name(self):
#         return self.full_name
