from django import forms
from django.contrib.auth.models import User
from job_scraping.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'width':'100%'}))
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('age','location','Gender','Job_Interests','Qualifications')
