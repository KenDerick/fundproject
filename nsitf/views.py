from django.shortcuts import render,redirect
from nsitf.forms import (EmployerRegForm,EmployerRegistrationForm)
from django.views.generic import FormView
from nsitf.models import (Employers,User,Local_Government,State,Regions,Branches)
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils import timezone
now = timezone.now()

def home(request):
    return render(request, 'nsitf/home.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')
    else:
        return render(request, 'nsitf/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('home')


def submit_new_employer(request):
    user_id=request.user.staff_id   #Get Cuurent User Staff Id
    staff_id= User.objects.all().get(staff_id=user_id)  #Convert This to A User Object
    fname=request.user.first_name
    lname=request.user.last_name
    fullname = fname + ' ' + lname  #Concantenate first and last name
    # state_id = request.GET.get('state')
    # local_governments = Local_Government.objects.filter(state_id=state_id).order_by('name')  
    form = EmployerRegistrationForm()
   
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST or None)
       
        if form.is_valid():
            name=form.cleaned_data['name']                       
            CAC_no = form.cleaned_data['CAC_no']
            branch = form.cleaned_data['branch']
            region = form.cleaned_data['region']
            address1=form.cleaned_data['address1']
            house_no=form.cleaned_data['house_no']
            street=form.cleaned_data['street']
            local_council=form.cleaned_data['local_council']
            state=form.cleaned_data['state']
                                 
            newemployer=Employers(name=name,CAC_no=CAC_no,state=state,\
            branch=branch,address1=address1,house_no=house_no,street=\
            street,local_council=\
            local_council,submitted_by=staff_id,region=region)
            
            newemployer.save()
            form = EmployerRegistrationForm(request.POST or None)
    
            messages.success(request, 'Your Leave Application has been saved!')
            return redirect('registrationsuccess')
                        
        else:
            messages.error(request, 'Your Application Was Not Saved!')
            form = EmployerRegistrationForm(request.POST or None)

    return render(request, 'nsitf/registrationpage.html', {'form':form})


def registration_success (request):
    user = request.user.staff_id
    submitted_by=User.objects.get(staff_id=user)
    thisemployer=Employers.objects.filter(submitted_by__exact=submitted_by)
    return render(request, 'nsitf/reg_confirm.html', {'thisemployer': thisemployer})