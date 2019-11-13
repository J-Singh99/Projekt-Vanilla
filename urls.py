from django.contrib import admin
from django.urls import path
from job_scraping import views
from django.conf.urls import include


urlpatterns= [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('registration/',views.registration,name='registration'),
    path('userhome/',views.userhome,name='userhome'),
    path('userlogout',views.userlogout,name="userlogout"),

    ]
