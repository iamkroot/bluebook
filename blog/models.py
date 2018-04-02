from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """Category of a resource."""
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'category_name': self.name})

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
    blacklist = models.ManyToManyField(Category, blank=True)

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'uname': self.user.username})

    def __str__(self):
        return self.user.username


class Post(models.Model):
    """Represents a resource post."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category, related_name='posts')
    author = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='posts'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Represents a comment to a post"""
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        Profile,
        related_name='comments',
        null=True,
        on_delete=models.SET_NULL
    )
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.content
