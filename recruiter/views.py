from django.shortcuts import render
from . import views
from .models import Job
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.shortcuts import render,HttpResponseRedirect
from DoubtApp.models import StudentRegister,UploadedDocument,Reviews_college,message_stud
from django.views.generic import ListView, CreateView, UpdateView
# Create your views here.
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone


class HomePage(CreateView):
	def get(self, request, *args, **kwargs):
  
		User = get_user_model()
		user_profile_id = request.user.id		
		full_details =StudentRegister.objects.get(user_id=user_profile_id)
		print(full_details)     
		return render(request,'recruits/homepage.html',{'full_details':full_details})

class AddJob(CreateView):
    def get(self, request, *args, **kwargs):
        User = get_user_model()
        user_profile_id = request.user.id
        full_details = StudentRegister.objects.get(user_id=user_profile_id)
        return render(request, 'recruits/add_job.html', {'full_details': full_details})

    def post(self, request, *args, **kwargs):
        User = get_user_model()
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        job_category = request.POST.get('job_category')
        job_requirements = request.POST.get('job_requirements')
        job_duration = request.POST.get('job_duration')
        job_budget = request.POST.get('job_budget')
        company_name = request.POST.get('company_name')
        company_website = request.POST.get('company_website')
        company_description = request.POST.get('company_description')
        contact_name = request.POST.get('contact_name')
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')
        job_posting = Job(
            job_title=job_title,
            job_description=job_description,
            job_category=job_category,
            job_requirements=job_requirements,
            job_duration=job_duration,
            job_budget=job_budget,
            company_name=company_name,
            company_website=company_website,
            company_description=company_description,
            contact_name=contact_name,
            contact_email=contact_email,
            contact_phone=contact_phone,
            recruiters=request.user,
            status=1
        )
        job_posting.save()

        return HttpResponseRedirect('/recruiter_stud/homepage')

class JobListing(CreateView):
    def get(self, request, *args, **kwargs):
        job_list = Job.objects.all()
        print("a")
        search_text = request.GET.get('search','')
        print(search_text)
        if search_text:
        	job_list=job_list.filter(Q(job_title__icontains=search_text))
        paginator = Paginator(job_list, 10) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            response = render_to_string('recruits/job_list_pagination.html', context)

            return JsonResponse(response, safe=False)
        
        return render(request, 'recruits/job_listing.html', context)

class AcceptReject(CreateView):
    def get(self, request, id):  
        User = get_user_model()
        user_profile_id = request.user.id       
        jobs_status = message_stud.objects.filter(Job_id=id).filter(Job_id__recruiters_id=user_profile_id).filter(Q(status= 0)| Q(status=1))         
        return render(request,'recruits/accept_reject.html',{'jobs_status':jobs_status}) 
    def post(self, request):
        print("dd")
        job_id = request.POST.get('job_id')
        print(job_id)
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')
        try:
            job = Job.objects.get(id=job_id, recruiters=request.user)
            student = User.objects.get(id=student_id)
            application = message_stud.objects.get(Job=job, students_ids=student)
            if action == 'accept':
                application.status = 1
                application.save()
                messages.success(request, f"{student.username}'s job application for {job.job_title} has been accepted.")
                response="Accepted"
                return JsonResponse(response, safe=False)
            elif action == 'reject':
                application.status = -1
                application.save()
                messages.warning(request, f"{student.username}'s job application for {job.job_title} has been rejected.")
                response="Reject"
                return JsonResponse(response, safe=False)
            else:
                messages.warning(request, "Invalid action.")
        except (Job.DoesNotExist, User.DoesNotExist, message_stud.DoesNotExist):
            messages.warning(request, "Invalid job or student.")
        return redirect('/recruiter_stud/accept_reject', id=job_id)        
