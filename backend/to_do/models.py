from django.db import models
from rest_framework.authtoken.admin import User


class Todo(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    completion_date = models.DateField()
    complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
