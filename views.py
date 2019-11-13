from django.shortcuts import render
from job_scraping.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from job_scraping.models import UserProfileInfo, Job_Details
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.template import RequestContext
from selenium import webdriver
from django.views.generic import ListView,DetailView
from django.utils.decorators import method_decorator
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException
import time
from bs4 import BeautifulSoup
import pandas as pd

# Create your views here.
def index(request):
    return render(request,'job_scraping/index.html')

def login(request):
    if request.method=='POST':
        df = pd.DataFrame(columns=('Username', 'Time'))
        uname=request.POST.get('username')
        passw=request.POST.get('password')
        user=authenticate(username=uname,password=passw)
        timing= time.localtime(time.time())
        csv_dict = [{'Username':uname, 'Time':timing}]
        temp_df_entry = pd.DataFrame(csv_dict)
        temp_df_entry.to_csv('login_info.csv')
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
    if request.method == "POST":
        driver = webdriver.Chrome(r"C:\Users\Dell\Downloads\chromedriver.exe")
        driver.get('https://www.indeed.com')
        driver.refresh()
        jobs = request.POST.get('job_name')
        loc = request.POST.get('city')
        print(jobs)
        print(loc)
        what = driver.find_element_by_id('text-input-what')
        where = driver.find_element_by_id('text-input-where')

        what.send_keys(Keys.CONTROL + "a")
        what.send_keys(Keys.DELETE)
        what.send_keys(jobs)

        where.send_keys(Keys.CONTROL + "a")
        where.send_keys(Keys.DELETE)
        where.send_keys(loc)
        where.send_keys(Keys.RETURN)
        df = pd.DataFrame(columns=('Job_Title', 'Company_Name', 'Location', 'Salary', 'Job_Summary'))
        count = 1
        total_pages = int(input('Enter the number of pages to iterate over. Below 5 works best.'))

        while count != total_pages:
            print('Page :', count)
            count = count + 1

            # Get source
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')

            # Make a SOUP iterable list
            SOUP_JOBS = soup.find_all(class_= 'jobsearch-SerpJobCard unifiedRow row result clickcard')
            # Make a SELENIUM iterable list
            SELENIUM_JOBS = driver.find_elements_by_xpath("//div[@class = 'location accessible-contrast-color-location']")


            # Max_iterator = len(SOUP_JOBS)
            iterator = 0

            # Run loop to store things in CSV
            for i in range(3) :


                # Make a SOUP iterable list
                SOUP_JOBS = soup.find_all(class_= 'jobsearch-SerpJobCard unifiedRow row result clickcard')

                # Make a SELENIUM iterable list
                SELENIUM_JOBS = driver.find_elements_by_xpath("//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard']")

                # Make variables to store info and use later
                Job_Title = SOUP_JOBS[i].find(attrs={'data-tn-element' : 'jobTitle'})['title']
                print(Job_Title)
                Company_Name = SOUP_JOBS[i].find(class_ = 'company').text

                Location = SOUP_JOBS[i].find(class_ = 'location accessible-contrast-color-location').text
                print(Location)
                Salary = 'NEGOTIABLE'
                if SOUP_JOBS[i].find(class_ = 'salaryText') != None:
                    Salary = SOUP_JOBS[i].find(class_ = 'salaryText').text
                print(Salary)
                Job_Summary = ''


                # Find card number
                index_num = iterator

                # Focus on element, click it
                SELENIUM_JOBS[index_num].click()

                # Only if new page has opened
                num_tabs = driver.window_handles
                if len(num_tabs) == 2:

                    # Switch to new tab
                    driver.switch_to_window(num_tabs[1])

                    # Find and store Job_Summary
                    Job_Summary = driver.find_element_by_xpath("//div[@class='jobsearch-ViewJobLayout-jobDisplay icl-Grid-col icl-u-xs-span12 icl-u-lg-span7']").text

                    # Move on in life
                    driver.close()
                    driver.switch_to_window(num_tabs[0])

                    if len(driver.window_handles) != 1:
                        print('OHHHHH!!! OHHHHHHHHHH!!! ERROR!!!!!!')
                        print('DROP EVERYTHING AND CALL HELP!!! THIS IS THE BIGGEST ERROR EVER!!!')
                        print('Please, PLEASE, call Jaspreet!')
                        break

                else:
                    print('OHHHHH!!! OHHHHHHHHHH!!! ERROR!!!!!!')
                    print('Please, PLEASE, call Jaspreet!')
                    break


                print(Company_Name)
                print(Job_Summary)
                #creating an entry to add to CSV file
                csv_dict = [{'Job_Title':Job_Title, 'Company_Name':Company_Name, 'Location':Location, 'Salary':Salary, 'Job_Summary':Job_Summary}]
                temp_df_entry = pd.DataFrame(csv_dict)
                b=Job_Details.objects.create(job_name=Job_Title, company_name=Company_Name, location=Location, salary=Salary, summary=Job_Summary)
                b.save()
                #pushing entry into CSV file
                df = df.append(temp_df_entry, ignore_index = True)
                df.to_csv('Go.csv')
                print(df.to_html())

                # Click the next page
                try:
                    next_page = driver.find_element_by_partial_link_text('Next ')
                    next_page.click()
                except ElementClickInterceptedException:
                    driver.find_element_by_partial_link_text('No, thanks').click()
                    print('Pop Up Closed!!')
                    next_page = driver.find_element_by_partial_link_text('Next ')
                    next_page.click()
                except:
                    pass

                iterator = iterator + 1

            driver.quit()
            return HttpResponseRedirect(reverse('listofjobs'))


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
        df = pd.DataFrame(columns=('username', 'age', 'Location', 'Gender', 'Job_Interests','Qualifications'))
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
            csv_dict = [{'username':user.username, 'age':age, 'Location':Location, 'Gender':Gender, 'Job_Interests':Job_Interests, 'Qualifications':Qualifications}]
            temp_df_entry = pd.DataFrame(csv_dict)
            temp_df_entry.to_csv('register.csv')
            return HttpResponseRedirect(reverse('login'))

    return render(request,'job_scraping/register.html', {'user_form':form} )

@method_decorator(login_required, name='dispatch')
class listofjobs(ListView):
    model=Job_Details
    context_object_name='Job_Details'
    template_name='job_scraping/listofjobs.html'

    def get_queryset(self):
        queryset = super(listofjobs, self).get_queryset()
        return queryset


@method_decorator(login_required, name='dispatch')
class Job_Detail(DetailView):
    model=Job_Details
    context_object_name='Job_Detailing'
    template_name='job_scraping/detail.html'
