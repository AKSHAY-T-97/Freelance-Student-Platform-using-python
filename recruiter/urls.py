from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from . import views
from django.contrib.auth.views import LoginView



urlpatterns =[

	path('homepage',views.HomePage.as_view()),
	path('add_job',views.AddJob.as_view()),						
	path('job_listing',views.JobListing.as_view()),
	path('accept_reject/<int:id>/',views.AcceptReject.as_view()),
	path('accept_reject',views.AcceptReject.as_view()),

]
