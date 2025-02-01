from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    TASK_TYPES = [
        ("priority", "Priority Task"),
        ("regular", "Regular Task"),
    ]

    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    metadata = models.JSONField(default=dict)

    def __str__(self):
        return self.title
