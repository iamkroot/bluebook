from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Tag(models.Model):
    """Tag of a resource."""
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """Profile of a user in the site."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    bio = models.TextField(max_length=500, blank=True)
    favorites = models.ManyToManyField(
        'Post',
        related_name='favorited_by',
        blank=True
    )
    blacklist = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Post(models.Model):
    """Represents a resource post."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='posts')
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('can_delete', 'Can delete the posts'),
        )
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title
