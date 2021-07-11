from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tasks_List(models.Model):
    task = models.CharField(max_length=1000)
    complete = models.BooleanField(default=False)
    logged_user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.task
