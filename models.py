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

class Job_Details(models.Model):
    job_name=models.CharField(max_length=100)
    company_name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    salary=models.CharField(max_length=100)
    summary=models.CharField(max_length=1000)

    def __str__(self):
        return self.job_name

class Sorted_Job_Details(models.Model):
    job_name=models.CharField(max_length=100)
    company_name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    salary=models.CharField(max_length=100)
    summary=models.CharField(max_length=1000)

    def __str__(self):
        return self.job_name
