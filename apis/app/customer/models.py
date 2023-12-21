from django.db import models


# Customer State
class CustomerState(models.Model):
    session_id = models.CharField(default='', max_length=100, primary_key=True)
    refresh_token = models.TextField(default='', unique=True)
    project_id = models.CharField(default='', max_length=100, unique=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)