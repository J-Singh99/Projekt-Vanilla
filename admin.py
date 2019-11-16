from django.contrib import admin
from job_scraping.models import UserProfileInfo, Job_Details, Sorted_Job_Details, Sorted_in_range

admin.site.register(Job_Details)
admin.site.register(Sorted_Job_Details)
admin.site.register(Sorted_in_range)
