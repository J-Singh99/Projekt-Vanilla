from django.shortcuts import render
from job_scraping.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from job_scraping.models import UserProfileInfo
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.template import RequestContext
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

import pandas as pd
list_cart=[]
# Create your views here.
def index(request):
    return render(request,'job_scraping/index.html')

def login(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        passw=request.POST.get('password')
        user=authenticate(username=uname,password=passw)
        if user:
            if user.is_active:
                auth_login(request,user)
                return HttpResponseRedirect(reverse('userhome'))
            else:
                return HttpResponse("User is inactive")
        else:
            return render(request,'job_scraping/login.html',{'err':'Invalid User Credentials!'})

    else:
        return render(request,'job_scraping/login.html')



@login_required

def userhome(request):

    if request.method=='POST':
        driver = webdriver.Chrome(r"C:\Users\Dell\Downloads\chromedriver.exe")
        driver.get('https://www.indeed.com')
        driver.refresh()
        jobs =request.POST.get('job_name')
        loc = request.POST.get('city')
        what = driver.find_element_by_id('text-input-what')
        where = driver.find_element_by_id('text-input-where')
        what.send_keys(Keys.CONTROL + "a")
        what.send_keys(Keys.DELETE)
        what.send_keys(jobs)
        where.send_keys(Keys.CONTROL + "a")
        where.send_keys(Keys.DELETE)
        where.send_keys(loc)
        where.send_keys(Keys.RETURN)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        list1=[]

        for i in soup.find_all(class_= 'jobsearch-SerpJobCard unifiedRow row result clickcard'):
            job_list=[]

            job_list.append(i.find(attrs={'data-tn-element' : 'jobTitle'})['title'])
            job_list.append(i.find(class_ = 'company').text)
            job_list.append(i.find(class_ = 'location accessible-contrast-color-location').text)
            if i.find(class_ = 'salaryText') == None:
                job_list.append('Not available')
            else:
                job_list.append(i.find(class_ = 'salaryText').text)


            list1.append(job_list)

        return render(request,'job_scraping/userhome.html',{'list1':list1})

    print(list_cart)
    return render(request,'job_scraping/userhome.html')

@login_required
def userlogout(request):
    logout(request)
    #redirect the user
    return HttpResponseRedirect(reverse('login'))


def registration(request):
    form_class = UserForm
    # if request is not post, initialize an empty form
    form = form_class(request.POST or None)
    registered=False
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            user=form.save()
            #hash the password
            user.set_password(user.password)
            #save
            user.save()
            age=request.POST.get('Age')
            Location=request.POST.get('Location')
            Gender=request.POST.get('Gender')
            Job_Interests=request.POST.get('Job_Interests')
            Qualifications=request.POST.get('Qualifications')
            b=UserProfileInfo.objects.create(age=age, location=Location, Gender=Gender, Job_Interests=Job_Interests, Qualifications=Qualifications, user=user)
            b.user=user
            b.save()
            return HttpResponseRedirect(reverse('login'))

    return render(request,'job_scraping/register.html', {'user_form':form} )
