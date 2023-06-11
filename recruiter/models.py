from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
import datetime
# Create your models here.
class Job(models.Model):
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    job_requirements = models.TextField()
    job_category=models.CharField(max_length=50)
    job_duration = models.CharField(max_length=50)
    job_budget = models.DecimalField(max_digits=8, decimal_places=2)
    company_name = models.CharField(max_length=100)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    contact_name = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True, editable=False)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    status =models.IntegerField(default=1)	
    recruiters = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
