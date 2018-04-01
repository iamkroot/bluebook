from django.views.generic import DetailView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView, FormView
)
from django.views.generic.base import RedirectView
from .models import Post, Profile, Category
from .forms import SignUpForm, AddFavorite
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseForbidden


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = get_object_or_404(Profile, user=self.request.user)
            initial = profile.favorites.filter(id=self.object.id).exists()
            context['form'] = AddFavorite(initial={'fav': initial})
        return context


class PostFavorite(SingleObjectMixin, FormView):
    model = Post
    template_name = 'blog/post_detail.html'
    form_class = AddFavorite

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):  # add or remove post from favorites
        profile = get_object_or_404(Profile, user=self.request.user)
        if not form.cleaned_data.get('fav'):
            self.object.favorited_by.remove(profile)
        else:
            self.object.favorited_by.add(profile)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.object.pk})


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


class SignUpView(FormView):
    template_name = 'account/signup.html'
    form_class = SignUpForm
    success_url = '/accounts/login'

    def form_valid(self, form):  # Save Profile bio to database
        user = form.save()
        user.refresh_from_db()
        user.profile.bio = form.cleaned_data.get('bio')
        user.save()
        return super().form_valid(form)


class RedirectLoggedInUserView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            'user-profile', kwargs={'uname': self.request.user.username})


class UserProfile(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'blog/profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['uname'])
