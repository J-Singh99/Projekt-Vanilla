from django.shortcuts import render
from job_scraping.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from job_scraping.models import UserProfileInfo, Job_Details, Sorted_Job_Details
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
    Job_Details.objects.all().delete()
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
        count = 0

        while count != 3:
            print('Page :', count)
            count = count + 1
            source = driver.page_source
            soup = BeautifulSoup(source, 'html.parser')
            SOUP_JOBS = soup.find_all(class_= 'jobsearch-SerpJobCard unifiedRow row result clickcard')
            SELENIUM_JOBS = driver.find_elements_by_xpath("//div[@class = 'location accessible-contrast-color-location']")
            iterator = 0
            print(len(SELENIUM_JOBS))
            for i in range(3) :
                SOUP_JOBS = soup.find_all(class_= 'jobsearch-SerpJobCard unifiedRow row result clickcard')
                SELENIUM_JOBS = driver.find_elements_by_xpath("//div[@class = 'jobsearch-SerpJobCard unifiedRow row result clickcard']")
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
                index_num = iterator
                try:
                    SELENIUM_JOBS[i].click()
                except ElementClickInterceptedException:
                    driver.find_element_by_partial_link_text('No, thanks').click()
                    print('Pop up closed while clicking card!!')
                    SELENIUM_JOBS[i].click()



                num_tabs = driver.window_handles
                if len(num_tabs) == 2:
                    driver.switch_to_window(num_tabs[1])
                    Job_Summary = driver.find_element_by_xpath("//div[@class='jobsearch-ViewJobLayout-jobDisplay icl-Grid-col icl-u-xs-span12 icl-u-lg-span7']").text
                    driver.close()
                    try:
                        driver.switch_to_window(num_tabs[0])
                    except ElementClickInterceptedException:
                        driver.find_element_by_partial_link_text('No, thanks').click()
                        print('Pop up closed while switching back!!')
                        driver.switch_to_window(num_tabs[0])


                    if len(driver.window_handles) != 1:
                        print('OHHHHH!!! OHHHHHHHHHH!!! ERROR!!!!!!')
                        break

                else:
                    print('OHHHHH!!! OHHHHHHHHHH!!! ERROR!!!!!!')
                    break

                print(Company_Name)
                print(Job_Summary)
                csv_dict = [{'Job_Title':Job_Title, 'Company_Name':Company_Name, 'Location':Location, 'Salary':Salary, 'Job_Summary':Job_Summary}]
                temp_df_entry = pd.DataFrame(csv_dict)
                b=Job_Details.objects.create(job_name=Job_Title, company_name=Company_Name, location=Location, salary=Salary, summary=Job_Summary)
                b.save()
                df = df.append(temp_df_entry, ignore_index = True)
                df.to_csv('God_Given_Gift.csv')
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


@method_decorator(login_required, name='dispatch')
class listofjobs_sorted(ListView):
    model=Sorted_Job_Details
    context_object_name='Sorted_Job_Details'
    template_name='job_scraping/listofjobs_sorted.html'

    def get_queryset(self):
        queryset = super(listofjobs_sorted, self).get_queryset()
        return queryset

def sorting(request):

    Sorted_Job_Details.objects.all().delete()
    model=Sorted_Job_Details
    context_object_name='Sorted_Job_Details'
    template_name='job_scraping/listofjobs_sorted.html'
    df = pd.read_csv('God_Given_Gift.csv')
    df = df.drop("Unnamed: 0", axis=1)
    df.loc[df.Salary == 'NEGOTIABLE', 'Salary'] = 0
    Min_Salary = []
    Max_Salary = []

    for sal in df['Salary']:
        sal=str(sal)
        print(sal)
        if sal =='0':
            Max_Salary.append(0)

        if 'month' in sal:
            start_index=sal.find('-')
            if '-' in sal:
                print('hi')
                end_index=sal.find('a')
                str_final=sal[start_index+3:end_index-1]
                str_final=str_final.replace(',','')
                str_int_final=float(str_final)
                Max_Salary.append(str_int_final)

            if '-' not in sal:
                end_index=sal.find('a')
                str_final=sal[2:end_index-1]
                str_final=str_final.replace(',','')
                str_int_final=float(str_final)
                Max_Salary.append(str_int_final)


        if 'year' in sal:
            if '-' in sal:
                start_index=sal.find('-')
                end_index=sal.find('a')
                str_final=sal[start_index+3:end_index-1]
                str_final=str_final.replace(',','')
                str_int_final=float(str_final)/12
                Max_Salary.append(str_int_final)


            if '-' not in sal:
                end_index=sal.find('a')
                str_final=sal[2:end_index-1]
                str_final=str_final.replace(',','')
                str_int_final=float(str_final)/12
                Max_Salary.append(str_int_final)


    print(Max_Salary)
    df['Max_Salary']= Max_Salary
    df.sort_values('Max_Salary', ascending=False, inplace=True)
    print(df)

    for i in range(0,df.shape[0]):
        b=Sorted_Job_Details.objects.create(job_name=df.iloc[i][0], company_name=df.iloc[i][1], location=df.iloc[i][2], salary=df.iloc[i][3], summary=df.iloc[i][4])
        b.save()
    return render(request,'job_scraping/intermediate.html')
