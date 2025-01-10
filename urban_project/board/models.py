from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ad_images/', null=True, blank=True,  storage=FileSystemStorage())
    likes = models.ManyToManyField(User, related_name='liked_advertisements', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_advertisements', blank=True)



    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def get_stats(self):
        return {
            'created_advertisements': self.author.profile.get_stats().get('created_advertisements', 0),
            'total_likes': self.author.profile.get_stats().get('total_likes', 0),
            'total_dislikes': self.author.profile.get_stats().get('total_dislikes', 0),
        }

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    created_advertisements = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f'Profile for {self.user.username}'

    def get_stats(self):
        return {
            'created_advertisements': self.created_advertisements,
            'total_likes': self.total_likes,
            'total_dislikes': self.total_dislikes,
        }

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_user_profile_for_existing_users(sender, instance, created, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Advertisement)
def update_advertisement_stats(sender, instance, created, **kwargs):
    if created:
        instance.author.profile.created_advertisements += 1
        instance.author.profile.save()
    elif instance.pk:
        instance.author.profile.total_likes += instance.likes.count() - Advertisement.objects.get(pk=instance.pk).likes.count()
        instance.author.profile.total_dislikes += instance.dislikes.count() - Advertisement.objects.get(pk=instance.pk).dislikes.count()
        instance.author.profile.save()

@receiver(pre_delete, sender=Advertisement)
def delete_advertisement_stats(sender, instance, **kwargs):
    instance.author.profile.created_advertisements -= 1
    instance.author.profile.total_likes -= instance.likes.count()
    instance.author.profile.total_dislikes -= instance.dislikes.count()
    instance.author.profile.save()



class Comment(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.advertisement}'