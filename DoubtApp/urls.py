from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from . import views
from django.contrib.auth.views import LoginView



urlpatterns =[

	path('studentregister',views.StudentRegisters.as_view()),
	path('studentlogin',views.StudentLogin.as_view()),
	path('profile',views.StudentProfile.as_view()),
	path('index',views.IndexPage.as_view()),
	path('document_uploads',views.Document_uploads.as_view()),
	path('reviews',views.Reviews.as_view()),	
	path('search_job',views.SearchJob.as_view()),			
	path('logout',views.LogOut),
	path('forgot-password/', views.forgot_password, name='forgot_password'),
	path('messages', views.send_message, name='send_message'),	
	path('accepted_job',views.MyJobsAccepted.as_view()),
	path('change_password',views.ChangePassword.as_view(),name="change_password"),															
]
