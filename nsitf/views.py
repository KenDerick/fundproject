from django.shortcuts import render,redirect
from nsitf.forms import (AddNewUserForm, SignUpForm, EmployerRegistrationForm)
from django.views.generic import FormView
from nsitf.models import * #(AllStaff,Employers,User,Local_Government,State,Regions,Branches,CAC_DB,Registration_Status,)
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse


now = timezone.now()

def home(request):
    return render(request, 'nsitf/home.html', {})


def addnewuser(request):
    if request.method == 'POST':
        form = AddNewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = AddNewUserForm()
    return render(request,'nsitf/addnewuser.html',{'form':form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_id=form.cleaned_data['staff_id']
            form.save()
            user_object=User.objects.get(staff_id=user_id)
            user_details=AllStaff.objects.get(staff_id=user_id)
            # print(user_details)
            # print(user_object)
            # # for u in user_details:
            # #     user_id=u.staff_id

            if  not user_details:
                messages.error(request, "Sorry, We couldn't Find the Staff ID {} In Our Database, Please contact AdminHr".format(user_id))
                form = SignUpForm(request.POST)
            else:
                first_name=user_details.first_name
                middle_name=user_details.middle_name
                last_name=user_details.last_name
                if middle_name == None:
                    middle_name=''
                full_name='{} {} {}'.format(last_name,first_name,middle_name)
                staff_id=user_details.staff_id
                branch=user_details.branch
                is_Entry_staff = user_details.is_Entry_staff
                is_Approval_manager = user_details.is_Approval_manager 
                is_Sys_admin = user_details.is_Sys_admin
                messages.success(request, 'User Details Added!!')
                User.objects.filter(pk=staff_id).update(first_name=first_name,last_name=last_name,branch=branch,\
                    middle_name=middle_name,display_name=full_name,is_Entry_staff=is_Entry_staff,\
                    is_Approval_manager=is_Approval_manager,is_Sys_admin=is_Sys_admin)

                return redirect('home')
    else:
        form = SignUpForm()
    return render(request,'nsitf/signup.html',{'form':form})



def submit_new_employer(request):
    if request.user.is_authenticated:
        user_id=request.user.staff_id   #Get Curent User Staff Id
        staff_id= User.objects.all().get(staff_id=user_id)  #Convert This to A User Object
    else:
        staff_id = None

    form = EmployerRegistrationForm()

    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST or None)
       
        if form.is_valid():
            business_type= form.cleaned_data['business_type']
            employer_name=form.cleaned_data['employer_name']                       
            CAC_no = form.cleaned_data['CAC_no']
            CAC_reg_date = form.cleaned_data['CAC_reg_date']
            address=form.cleaned_data['address']
            house_no=form.cleaned_data['house_no']
            street=form.cleaned_data['street']
            district=form.cleaned_data['district']
            state=form.cleaned_data['state']
            local_council=form.cleaned_data['local_council']
            postal_address = form.cleaned_data['postal_address']
            Telephone1 = form.cleaned_data['Telephone1']
            Telephone2 = form.cleaned_data['Telephone2']
            email = form.cleaned_data['email']
            branch = form.cleaned_data['branch']
            region = form.cleaned_data['region']
                           
            newemployer=Employers(business_type= business_type,employer_name=employer_name,CAC_no=CAC_no,CAC_reg_date=CAC_reg_date,\
                        address=address,house_no=house_no,street=street,district=district,state=state,local_council=local_council,\
                        postal_address=postal_address,Telephone1=Telephone1,Telephone2=Telephone2,email=email,submitted_by=staff_id,\
                        submitted_on=now,branch=branch,region=region)
            
            newemployer.save()
            form = EmployerRegistrationForm(request.POST or None)
    
            messages.success(request, 'Your Leave Application has been saved!')
            return redirect('reg_details')
                        
        else:
            messages.error(request, 'Your Application Was Not Saved!')
            form = EmployerRegistrationForm(request.POST or None)

    return render(request, 'nsitf/registrationpage.html', {'form':form})



def details_dashboard (request):
    user = request.user.staff_id
    submitted_by=User.objects.get(staff_id=user)
    current_detail=Employers.objects.filter(submitted_by__exact=submitted_by)
    current_detail = current_detail.exclude(status__gt = 1)
    return render(request, 'nsitf/reg_details.html', {'current_detail': current_detail})


def cancel_registration(request, pk):
    user=request.user.staff_id      #Staff Id Of The Person Canceling
    cancelled_by= User.objects.get(staff_id=user)
    status_code = Registration_Status.objects.get(pk=6)
    Employers.objects.filter(employer_code=pk).update(status=status_code,cancelled_by\
    =cancelled_by,last_changed_by=user,)
    return redirect('mycancelledregistrations')

def cancelled_registrations(request):
    user=request.user.staff_id       #Staff Id Of The Person Canceling
    cancelled_by= User.objects.get(staff_id=user)
    status_code = Registration_Status.objects.get(pk=6)
    cancelled_registrations=Employers.objects.filter(submitted_by__exact=cancelled_by, status__exact=6)
    return render(request, 'nsitf/cancelled_registrations.html', {'cancelled_registrations': cancelled_registrations})



def registration_success (request):
    if request.user.is_authenticated:
        user = request.user.staff_id
        submitted_by=User.objects.get(staff_id=user)
        thisemployer=Employers.objects.filter(submitted_by__exact=submitted_by)
        return render(request, 'nsitf/reg_confirm.html', {'thisemployer': thisemployer})

  
def search_cac(request):
    if request.method == "GET" and request.is_ajax():
        cac_no = request.GET.get('cac_no', None)

        try:
            employer = CAC_DB.objects.get(cac_no=cac_no)

        except:
            return JsonResponse({"success": False}, status=400)
        company_info = {
            "Company_RC": employer.cac_no,
            "Company_Name": employer.company_name,
            "Company_Address": employer.address,
            "Company_RegDate": employer.Reg_date,
        }

        return JsonResponse({"company_info": company_info}, status=200)

    return JsonResponse({"success": False}, status=400)
    

def route_tasks(request,pk):      #view to sumbmit registration and route it to the appropriate task queue
    user = request.user.staff_id  # GetThe Logged On Users' Staff id
    sent_by = User.objects.get(staff_id=user)   # make the staffid above a user object
    regpk = Employers.objects.all().get(employer_code=pk)
    name = regpk.employer_name
    CAC_no = regpk.CAC_no
    CAC_reg_date = regpk.CAC_reg_date
    status = regpk.status
    employer_branch = regpk.branch
    approval_BM_ID = Reg_Task_Route.objects.all().get(branch=employer_branch)
    approval_BM = approval_BM_ID.approval_queue
    status = Registration_Status.objects.get(pk=2)
    new_task = Reg_Tasks(code=regpk, queue_code=approval_BM, name=name, CAC_no=CAC_no,CAC_reg_date=CAC_reg_date,\
              sent_by=sent_by,sent_on=now,status=status, branch=employer_branch)
    new_task.save()
    Employers.objects.filter(pk=pk).update(status=status)       # Update the rgistrations Status in the Employer's table
    return redirect('reg_details')

def task_queues_view(request):
    user = request.user.staff_id
    taskviewowner = User.objects.get(staff_id=user)
    my_queue_code = taskviewowner.branch_id
    my_tasks = Reg_Tasks.objects.filter(queue_code_id=my_queue_code)
    print(my_tasks)
    return render(request, 'nsitf/taskqueue.html', {'my_tasks': my_tasks}) 