from django.shortcuts import render,redirect,HttpResponseRedirect, get_object_or_404, HttpResponse
from nsitf.forms import (AddNewUserForm, SignUpForm, EditRegistrationForm,PartOneEmployerForm, PartTwoEmployerForm)
from django.views.generic import FormView
from nsitf.models import * #(AllStaff,Employers,User,Local_Government,State,Regions,Branches,CAC_DB,Registration_Status,)
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
# from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
import csv
import io
import smtplib

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
        form = EmployerRegistrationForm(request.POST or None, request.FILES)
       
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
            employee_list= form.cleaned_data['employee_list']

            newemployer=Employers(business_type= business_type,employer_name=employer_name,CAC_no=CAC_no,CAC_reg_date=CAC_reg_date,\
                        address=address,house_no=house_no,street=street,district=district,state=state,local_council=local_council,\
                        postal_address=postal_address,Telephone1=Telephone1,Telephone2=Telephone2,email=email,submitted_by=staff_id,\
                        submitted_on=now,branch=branch,region=region,employee_list=employee_list)
            
            newemployer.save()
            form = EmployerRegistrationForm(request.POST or None)
    
            messages.success(request, 'Your Leave Application has been saved!')
            return redirect('reg_details')
                        
        else:
            messages.error(request, 'Your Application Was Not Saved!')
            form = EmployerRegistrationForm(request.POST or None)

    return render(request, 'nsitf/registrationpage.html', {'form':form})



def employerformone(request):
    if request.user.is_authenticated:
        user_id=request.user.staff_id                       #Get Curent User Staff Id
        staff_id= User.objects.all().get(staff_id=user_id)  #Convert This to A User Object
    else:
        staff_id = None

    form = PartOneEmployerForm()

    if request.method == 'POST':
        form = PartOneEmployerForm(request.POST or None)
        
        if form.is_valid():
            employer_name=form.cleaned_data['employer_name']                       
            CAC_no = form.cleaned_data['CAC_no']
            CAC_reg_date = form.cleaned_data['CAC_reg_date']
            save_msg = "You Have Successfully Commenced Employer Registration For {}\
        Please Enter Employer Location Details".format(employer_name)          
            partialnewemployer=Employers(employer_name=employer_name,CAC_no=CAC_no,\
            CAC_reg_date=CAC_reg_date,submitted_by=staff_id,submitted_on=now)               
                        
            partialnewemployer.save()
            messages.info(request, save_msg)
            return redirect('partialformtwo', partialnewemployer.pk)
                        
        else:
            messages.error(request, 'Your Application Was Not Saved!')
            form = PartOneEmployerForm(request.POST or None)

    return render(request, 'nsitf/registrationpage.html', {'form':form})


def employerformtwo(request,pk):
    if request.user.is_authenticated:
        user_id = request.user.staff_id                      # Get Curent User Staff Id
        staff_id = User.objects.all().get(staff_id=user_id)  # Convert This to A User Object
    else:
        staff_id = None

    thisemployer = get_object_or_404(Employers, pk=pk)

    form = PartTwoEmployerForm(request.POST or None, instance=thisemployer)

    if request.method == 'POST':
        form = PartTwoEmployerForm(request.POST or None, instance=thisemployer)

        if form.is_valid():
            business_type = form.cleaned_data['business_type']
            address = form.cleaned_data['address']
            house_no = form.cleaned_data['house_no']
            street = form.cleaned_data['street']
            district = form.cleaned_data['district']
            state = form.cleaned_data['state']
            local_council = form.cleaned_data['local_council']
            postal_address = form.cleaned_data['postal_address']
            Telephone1 = form.cleaned_data['Telephone1']
            Telephone2 = form.cleaned_data['Telephone2']
            email = form.cleaned_data['email']
            branch = form.cleaned_data['branch']
            region = form.cleaned_data['region']

            Employers.objects.filter(pk=pk).update(business_type = business_type, address=address,\
            house_no=house_no, street=street, district=district, state=state, \
            local_council=local_council,postal_address=postal_address, \
            Telephone1=Telephone1, Telephone2=Telephone2, email=email, \
            submitted_by=staff_id,submitted_on=now, branch=branch, region=region)

            form = PartTwoEmployerForm(request.POST or None)
            
            messages.success(request, 'Your employer registration has been saved!')
            return redirect('employee_upload', pk)
            # return redirect('reg_details')

        else:
            messages.error(request, 'Your Application Was Not Saved!')
            form = PartTwoEmployerForm(request.POST or None,instance=thisemployer)

    return render(request, 'nsitf/registrationpage2.html', {'form': form,'pk':pk})


def employee_upload(request,pk):
    thispk = Employers.objects.all().get(pk=pk)
    template = "nsitf/employee_upload.html"     # declaring template
    data = Employees.objects.all()
    # prompt is a context variable that can have different values depending on their context
    prompt = {
        'order': 'Order of the CSV should be first_name, last_name, other_names, email, address, phone, profile',
        'profiles': data
    }
    if request.method == "POST":
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        #first for loop to check through the data and ensure values are correct
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            print(type(column[5]))
            try:
                int(column[5])
            except Exception as e:
                logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
                messages.error(request,"You have some incorrect details in your file:: "+repr(e))
                return render(request, template, prompt)

        #second for loop to save the employees
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            print(column[1])
            _, created = Employees.objects.update_or_create(
                first_name=column[0],
                last_name=column[1],
                other_names=column[2],
                email=column[3],
                address=column[4],
                phone=column[5],
                employer_numb=thispk
            )
        context = {}
        return redirect('details_dashboard')
    return render(request, template, prompt)

#view for Cac data autofill
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


#view for Entry_person to see the details of the entry before submiting.
def details_dashboard (request):
    if request.user.is_authenticated:
        user_id = request.user.staff_id                      # Get Curent User Staff Id
        staff_id = User.objects.all().get(staff_id=user_id)  # Convert This to A User Object
        submitted_by=User.objects.get(staff_id=user_id)
    else:
        staff_id = None
        submitted_by = None

    current_detail=Employers.objects.filter(submitted_by__exact=submitted_by)
    current_detail = current_detail.exclude(status__gt = 1)
    return render(request, 'nsitf/reg_details.html', {'current_detail': current_detail})


#view for entry_staff to edit the data he has entered before submiting.
def edit_registration(request,pk):
    if request.user.is_authenticated:
        user_id = request.user.staff_id                     
        staff_id = User.objects.all().get(staff_id=user_id)  
    else:
        staff_id = None

    thisemployer = get_object_or_404(Employers, pk=pk)
    form = EditRegistrationForm(request.POST or None, instance=thisemployer)
    
    if request.method == 'POST':
        form = EditRegistrationForm(request.POST or None, instance=thisemployer)
        if form.is_valid():
            business_type= form.cleaned_data['business_type']
            employer_name=form.cleaned_data['employer_name']                       
            CAC_no = form.cleaned_data['CAC_no']
            CAC_reg_date = form.cleaned_data['CAC_reg_date']
            address = form.cleaned_data['address']
            house_no = form.cleaned_data['house_no']
            street = form.cleaned_data['street']
            district = form.cleaned_data['district']
            state = form.cleaned_data['state']
            local_council = form.cleaned_data['local_council']
            postal_address = form.cleaned_data['postal_address']
            Telephone1 = form.cleaned_data['Telephone1']
            Telephone2 = form.cleaned_data['Telephone2']
            email = form.cleaned_data['email']
            branch = form.cleaned_data['branch']
            region = form.cleaned_data['region']

            Employers.objects.filter(pk=pk).update(business_type = business_type,employer_name=employer_name,\
            CAC_no=CAC_no,CAC_reg_date=CAC_reg_date,address=address,house_no=house_no, street=street,\
            district=district, state=state,local_council=local_council,postal_address=postal_address,\
            Telephone1=Telephone1, Telephone2=Telephone2, email=email,submitted_by=staff_id,submitted_on=now,\
            branch=branch, region=region)

            form = EditRegistrationForm(request.POST or None)
            messages.success(request, 'Your Leave Application has been saved!')
            return redirect('details_dashboard')
            # return redirect('reg_details')

        else:
            messages.error(request, 'Your Application Was Not Saved!')
            form = EditRegistrationForm(request.POST or None,instance=thisemployer)
    return render(request, 'nsitf/edit_registration.html', {'form': form,'pk':pk})


#view for entry_staff to cancell an application
def cancel_registration(request, pk):
    if request.user.is_authenticated:
        user_id = request.user.staff_id                      #Staff Id Of The Person Canceling
        staff_id = User.objects.all().get(staff_id=user_id)  # Convert This to A User Object
        cancelled_by = User.objects.get(staff_id=user_id)
    else:
        staff_id = None
        cancelled_by = None
    
    status_code = Registration_Status.objects.get(pk=6)
    Employers.objects.filter(id=pk).update(status=status_code,cancelled_by=cancelled_by,last_changed_by=staff_id)
    return redirect('mycancelledregistrations')


#view for Entry_staff to see registrations he cancelled
def cancelled_registrations(request):
    if request.user.is_authenticated:
        user_id = request.user.staff_id                      # Get Curent User Staff Id
        staff_id = User.objects.all().get(staff_id=user_id)  # Convert This to A User Object
        cancelled_by= User.objects.get(staff_id=user_id)
    else:
        staff_id = None
        cancelled_by = None
    
    status_code = Registration_Status.objects.get(pk=6)
    cancelled_registrations=Employers.objects.filter(submitted_by__exact=cancelled_by, status__exact=6)
    return render(request, 'nsitf/cancelled_registrations.html', {'cancelled_registrations': cancelled_registrations})


# def registration_success (request):
#     if request.user.is_authenticated:
#         user = request.user.staff_id
#         submitted_by=User.objects.get(staff_id=user)
#         thisemployer=Employers.objects.filter(submitted_by__exact=submitted_by)
#         return render(request, 'nsitf/reg_confirm.html', {'thisemployer': thisemployer})

  
#view to sumbmit registration and route it to the appropriate task queue
def route_tasks(request,pk):      
    if request.user.is_authenticated:
        user_id = request.user.staff_id                      # Get Curent User Staff Id
        staff_id = User.objects.all().get(staff_id=user_id)  # Convert This to A User Object
        sent_by= User.objects.get(staff_id=user_id)
    else:
        staff_id = None
        sent_by = None

    regpk = Employers.objects.all().get(id=pk)
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
    return redirect('details_dashboard')


#Approval_manager to see his task queue
def task_queues_view(request):  
    user = request.user.staff_id
    taskviewowner = User.objects.get(staff_id=user)
    my_queue_code = taskviewowner.branch_id
    my_tasks = Reg_Tasks.objects.filter(queue_code_id=my_queue_code,status=2)
    print(my_tasks)
    return render(request, 'nsitf/taskqueue.html', {'my_tasks': my_tasks}) 


#Approval_manager to view the details of a task on his task_queue
def task_details_view(request, pk): 
    user = request.user.staff_id
    taskviewowner = User.objects.get(staff_id=user)
    this_task = Reg_Tasks.objects.get(code_id=pk)
    this_employer= Employers.objects.get(id=pk)
    print (this_employer)
    return render(request, 'nsitf/task_detail.html', {'this_employer':this_employer})


#Approval_manager to return a fualted task
def return_registration(request, pk):
    Employers.objects.filter(pk=pk).update(status=1)
    Reg_Tasks.objects.filter(pk=pk).update(status=1)
    return redirect('taskqueueview')


def approve_registration(request, pk):
    employer = Employers.objects.get(pk=pk)
    employer_email = employer.email
    approved = Registration_Status.objects.get(pk=5)
    html_message = render_to_string('nsitf/mail_template.html', {'employer': employer})
    plain_message = strip_tags(html_message)
    mail.send_mail('subject', plain_message, 'akorneth16@gmail.com', [employer_email], html_message=html_message)
    employer.status=approved
    employer.save()
    Reg_Tasks.objects.filter(pk=pk).update(status=approved)
    return redirect('taskqueueview')

def mail_template(request):
     return render(request, 'nsitf/mail_template.html')