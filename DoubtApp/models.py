from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from recruiter.models import Job
# Create your models here.




class StudentRegister(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    address = models.TextField()
    gender = models.CharField(max_length=10)
    course = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    type_student_rec = models.CharField(max_length=100)		



class UploadedDocument(models.Model):
    title = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to='uploaded_documents/')

    def __str__(self):
        return self.title    

class Reviews_college(models.Model):
    school_name = models.CharField(max_length=200)
    board = models.CharField(max_length=100)
    rating = models.IntegerField()
    review = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.school_name
 
class message_stud(models.Model):
    Job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True) 
    messages = models.TextField(null=True, blank=True)

    students_ids = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status =models.IntegerField(default=0)
    confirmation =models.IntegerField(default=0)