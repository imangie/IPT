from django.urls import path
from . import views
from .views import AdminPostEditView

urlpatterns = [
    path('users/', views.get_users, name='get_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<int:id>/', views.update_user, name='update_user'),
    path('users/delete/<int:id>/', views.delete_user, name='delete_user'),
    path('<int:post_id>/edit/', AdminPostEditView.as_view(), name='admin_post_edit'),
]

