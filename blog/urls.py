from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post-list'),
    path('post/<pk>/', views.PostDetail.as_view(), name='post-detail'),
    path('post/add', views.PostCreate.as_view(), name='post-new'),
    path('post/<pk>/update', views.PostUpdate.as_view(), name='post-update'),
    path('post/<pk>/delete', views.PostDelete.as_view(), name='post-delete'),
    path('tag/<tag_name>', views.TagDetail.as_view(), name='tag-detail')
]
