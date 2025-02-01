from django.urls import path
from .views import CreateTaskView

urlpatterns = [
    path('create/', CreateTaskView.as_view(), name='create_task'),
]
