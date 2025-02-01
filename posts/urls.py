from django.urls import path
from . import views
from .views import AdminPostEditView
from .views import CreatePostView

urlpatterns = [
path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<int:id>/', views.update_user, name='update_user'),
    path('users/delete/<int:id>/', views.delete_user, name='delete_user'),
    path('<int:post_id>/edit/', AdminPostEditView.as_view(), name='admin_post_edit'),
    path('posts/create/', CreatePostView.as_view(), name='create_post'),
]



