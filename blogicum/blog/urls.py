from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/', views.CategoryPosts.as_view(),
         name='category_posts',
         ),
    # ---
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', views.PostEditView.as_view(), name='edit_post'),
    path('posts/<int:pk>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('posts/<int:post_id>/comment/<int:pk>/edit_comment/',
         views.EditComment.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/comment/<int:pk>/delete_comment/',
         views.DeleteComment.as_view(),
         name='delete_comment'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/',
         views.EditProfile.as_view(),
         name='edit_profile'),
]
'''path('profile/<str:username>/',
         views.PostProfileView.as_view(),
         name='profile'),'''