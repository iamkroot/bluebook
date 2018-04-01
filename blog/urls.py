from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post-list'),
    re_path(
        r'^post/(?P<pk>\d+)/$',
        views.PostDetail.as_view(),
        name='post-detail'
    ),
    re_path(r'^post/create/$', views.PostCreate.as_view(), name='post-create'),
    re_path(
        r'^post/(?P<pk>\d+)/update/$',
        views.PostUpdate.as_view(),
        name='post-update'
    ),
    re_path(
        r'^post/(?P<pk>\d+)/delete/$',
        views.PostDelete.as_view(),
        name='post-delete'
    ),
    re_path(
        r'^post/(?P<pk>\d+)/addfav/$',
        views.PostFavorite.as_view(),
        name='post-add-fav'
    ),
    re_path(
        r'^category/(?P<category_name>[-\w]+)/$',
        views.CategoryDetail.as_view(),
        name='category-detail'
    ),
    re_path(
        r'^(accounts/)?profile/$',
        views.RedirectLoggedInUserView.as_view(),
        name='redirect-to-own-profile'
    ),
    re_path(
        r'^profile/(?P<uname>[\w.@+-]*)/$',
        views.UserProfile.as_view(),
        name='user-profile'
    ),
    re_path(
        r'^accounts/login/$',
        auth_views.LoginView.as_view(template_name='account/login.html')
    ),
    re_path(
        r'^accounts/signup/$',
        views.SignUpView.as_view(),
        name='user-signup'
    ),
]
