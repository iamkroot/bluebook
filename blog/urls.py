from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post-list'),
    path('post/<pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('post/create', views.PostCreate.as_view(), name='post-create'),
    path('post/<pk>/update', views.PostUpdate.as_view(), name='post-update'),
    path('post/<pk>/delete', views.PostDelete.as_view(), name='post-delete'),
    path('tag/<tag_name>', views.TagDetail.as_view(), name='tag-detail'),
    path('profile/<uname>', views.UserProfile.as_view(), name='user-profile'),
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='account/login.html')
    ),
]
