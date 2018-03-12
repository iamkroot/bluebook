from django.contrib import admin
from .models import Tag, Profile, Post

# Register your models here.
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Post)
