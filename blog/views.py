from django.views.generic import DetailView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Profile, Category
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostEditTestMixin(UserPassesTestMixin):
    """Permission mixin to test if the user can update/delete the post."""

    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.groups.filter(name='Moderator').exists():
            return True
        current_profile = get_object_or_404(Profile, user=self.request.user)
        return self.get_object().author == current_profile


class PostList(ArchiveIndexView):
    """List of recent posts."""
    model = Post
    date_field = 'pub_date'
    template_name = 'blog/post_list.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'categories']

    def form_valid(self, form):
        form.instance.author = get_object_or_404(
            Profile, user=self.request.user)
        return super().form_valid(form)


class PostUpdate(PostEditTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'categories']


class PostDelete(PostEditTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post-list')


class CategoryDetail(DetailView):
    template_name = 'blog/category_detail.html'

    def get_object(self):
        cat_name = self.kwargs['category_name']
        return get_object_or_404(Category, name__iexact=cat_name)


class AccountProfile(LoginRequiredMixin, DetailView):
    """Private profile of the user."""
    template_name = 'account/account_profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class UserProfile(LoginRequiredMixin, DetailView):
    """Public profile of the user."""
    model = Profile
    template_name = 'blog/profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['uname'])
