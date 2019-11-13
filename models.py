from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    age=models.CharField(max_length=10)
    location=models.CharField(max_length=100)
    Gender=models.CharField(max_length=10)
    Job_Interests=models.CharField(max_length=100)
    Qualifications=models.CharField(max_length=100)


    def __str__(self):
        return self.user.username
