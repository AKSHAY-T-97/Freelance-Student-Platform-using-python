from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
import smtplib

from .models import StudentRegister, UploadedDocument, Reviews_college, message_stud
from recruiter.models import Job



class IndexPage(CreateView):
    def get(self, request, *args, **kwargs):
        return render(request,'index/index.html')

class StudentRegisters(CreateView):
    model = StudentRegister
    fields = ['name', 'email', 'phone', 'dob', 'address', 'gender', 'course', 'college','type_student_rec']
    template_name = 'register.html'

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        name = request.POST.get('name')
        email = request.POST.get('email')
        auth_password = make_password(password)
        auth = User(password=auth_password, email=email, username=name)
        auth.save()
        user_id = auth.id
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course = request.POST.get('course')
        college = request.POST.get('college')
        types = request.POST.get('types')
        print(types)
        student = StudentRegister(name=name, email=email, user_id=user_id, phone=phone, dob=dob, address=address, gender=gender, course=course, college=college,type_student_rec=types)
        student.save()
        return JsonResponse({'status': 'success', 'message': 'Student registered successfully.'})



class StudentLogin(CreateView):
    model=User
    def get(self, request):
        message = request.GET.get('message', None)
        context = {'message': message}
        return render(request, 'login.html',context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password,backend='django.contrib.auth.backends.ModelBackend')
        print(user)
        if user is not None:

            if user.is_active:
                login(request, user)
                student_auth = StudentRegister.objects.get(user=user)
                if student_auth:
                    print(student_auth.type_student_rec)
                    if student_auth.type_student_rec=="recruiter":
                        return redirect("/recruiter_stud/homepage")
                    else:
                        return redirect("/student/profile")
                else:
                    return redirect("/student/studentregister")
            else:
                message="Unable to login to your account"
                return render(request,'login.html',{'message':message})
        else:
            message = "invalid username or password"
            return render(request,'login.html',{'message':message})

        return render(request, 'login.html')						

class StudentProfile(CreateView):
	def get(self, request ,*args, **kwargss):
		User = get_user_model()
		user_profile_id = request.user.id		
		full_details =StudentRegister.objects.get(user_id=user_profile_id)
		print(full_details)
		return render(request,'profile.html',{'full_details':full_details})

class Document_uploads(CreateView):
    def get(self, request, *args, **kwargss):
        return render(request, 'documents_upload.html')

    def post(self, request, *args, **kwargss):
        if request.method == 'POST':
            title = request.POST['title']
            file_type = request.POST['file-type']
            course = request.POST['course']
            university = request.POST['university']
            uploaded_file = request.FILES['file']
            document = UploadedDocument(title=title, file_type=file_type,
                                        course=course, university=university,
                                        uploaded_file=uploaded_file)
            document.save()

            messages.success(request, 'Document saved successfully.')
            return HttpResponseRedirect('/student/document_uploads')
        else:
            return render(request, 'upload.html')


class Reviews(CreateView):
    def get(self, request ,*args, **kwargs):
        print("dd")
        return render(request,'reviews.html')
    
    def post(self, request):
        if request.method == 'POST':
            # Get the values from the form
            school_name = request.POST.get('school-name')
            board = request.POST.get('board')
            rating = request.POST.get('rating')
            review = request.POST.get('comments')
            school_rating = Reviews_college(school_name=school_name, board=board, rating=rating, review=review)
            if request.user.is_authenticated:
                school_rating.author = request.user
            school_rating.save()
            messages.success(request, 'Review saved successfully.')
            return HttpResponseRedirect('/student/reviews')    
        return render(request, 'rate_school.html')    

def LogOut(request):
    logout(request)
    return HttpResponseRedirect('/student/index')


class SearchJob(CreateView):
    def get(self, request ,*args, **kwargs):
        job_list = Job.objects.all()
        print(job_list)
        search_text = request.GET.get('search','')
        job_category= request.GET.get('job_category','')
        if search_text:
            job_list=job_list.filter(Q(job_title__icontains=search_text))
        if job_category:
            job_list=job_list.filter(Q(job_category__icontains=job_category))
        print(job_list)    
        paginator = Paginator(job_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response = render_to_string('student_job_list_pagination.html', context)

            return JsonResponse(response, safe=False)
        return render(request,'student_job_serach.html',context)
        


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'})

        new_password = get_random_string(length=10)
        try:
            send_mail(
                'Password reset request',
                f'Your new password is: {new_password}',
                'your_gmail_address@gmail.com',
                [email],
                fail_silently=False,
                auth_user='',
                auth_password='', 
            )
        except smtplib.SMTPAuthenticationError as e:
            return JsonResponse({'status': 'error', 'message': 'Failed to authenticate with Gmail'})

        return JsonResponse({'status': 'ok', 'message': 'Password reset email sent'})

    return render(request, 'forgot_password_find.html')



def send_message(request):
    if request.method == 'POST':
        job_id = request.POST.get('jobs_id')
        print(job_id)
        message_text = request.POST.get('more_info')
        print(message_text)
        jobs = Job.objects.get(id=job_id)
        exits=message_stud.objects.filter(Job=jobs).filter(students_ids=request.user)
        if exits:
            messages.success(request, 'Already send once ...  Please wait ...')
        else:
            message = message_stud(Job=jobs,students_ids=request.user,messages=message_text)
            message.save()
            messages.success(request, 'Message sent successfully.')
        return redirect('/student/search_job')    

class MyJobsAccepted(CreateView):
    def get(self, request ,*args, **kwargs):
        my_id=request.user
        details=message_stud.objects.filter(students_ids=my_id).filter(status=1)
        return render(request,'my_accepted_job.html',{'details':details})



class ChangePassword(CreateView):
    template_name = 'change_password.html'

    def post(self, request, *args, **kwargs):
        print("Ddd")
        models = User
        current_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')
        user = request.user.id
        print(user)
        a = models.objects.get(id=user)        
        if not a.check_password(current_password):
            messages.error(request, 'Invalid current password.')
            return redirect('change_password')
            message = "Password changed successfully."
        else:
            a.password=make_password(new_password)
            a.save()
            message = "Password changed successfully."


        
        return JsonResponse({"message":message})
        
    def get(self, request, *args, **kwargs):
        id_user = request.user.id
        if id_user is not None:
            return render(request, "change_password.html")
        else:
            return JsonResponse({"message": "Error: User not authenticated."})
