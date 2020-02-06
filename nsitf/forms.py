from django import forms
from nsitf.models import (AllStaff,User,Employers,Employees,State,Branches,Regions,Local_Government,csv_upload)
from bootstrap_datepicker_plus import DatePickerInput
from django.contrib.auth.forms import UserCreationForm


class  AddNewUserForm(forms.ModelForm):

  class Meta():
    model = AllStaff
    fields = ('staff_id','email','first_name','middle_name','last_name','phone','region','state','branch','is_Entry_staff','is_Approval_manager','is_Sys_admin')


class SignUpForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    model = User
    fields = ('staff_id','email')

    widgets = {
      'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
      'email': forms.TextInput(attrs={'class': 'form-control'}),
      'password': forms.TextInput(attrs={'class': 'form-control'}),
    }


class PartOneEmployerForm(forms.ModelForm):
  CAC_no = forms.IntegerField(label="CAC Registration Number")
  employer_name = forms.CharField(label="Employer name")
  CAC_reg_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))

  class Meta:
    model = Employers
    fields = ['CAC_no','employer_name','CAC_reg_date',]


class PartTwoEmployerForm(forms.ModelForm):
  CAC_no = forms.IntegerField(label="CAC Registration Number")
  CAC_no.widget.attrs['readonly'] = True
  employer_name = forms.CharField(label="Employer name")
  employer_name.widget.attrs['readonly'] = True
  email = forms.EmailField(label=" Employer Email")
  address = forms.CharField(label="Address", required=False)
  house_no = forms.CharField(label="House No", required=False)
  street = forms.CharField(label="Street", required=False)
  postal_address = forms.CharField(label="Postal Address", required=False)
  Telephone1 = forms.IntegerField(label="Telephone1",required=False)
  Telephone2 = forms.IntegerField(label="Telephone2", required=False)
  types_of_businesses = [ 
    ('Public/Private Limited Company','Public/Private Limited Company'),
    ('Informal Sector Employer','Informal Sector Employer'),
    ('Partnership','Partnership'),
    ('Sole Proprietorship','Sole Proprietorship'),
    ('Others','Others')]
  business_type = forms.ChoiceField(choices=types_of_businesses, required=False, widget=forms.RadioSelect, label="Type Of Business")
  employer_name = forms.CharField(label="Employer name")

  class Meta:
    model = Employers
    fields = ['CAC_no', 'employer_name', 'business_type', 'email', 'address', 'house_no', 'district', 'street', 'state',
    'local_council','region','branch','postal_address','Telephone1','Telephone2']


class EditRegistrationForm(forms.ModelForm):
  CAC_no = forms.IntegerField(label="CAC Registration Number")
  types_of_businesses = [ 
    ('Public/Private Limited Company','Public/Private Limited Company'),
    ('Informal Sector Employer','Informal Sector Employer'),
    ('Partnership','Partnership'),
    ('Sole Proprietorship','Sole Proprietorship'),
    ('Others','Others')]
  business_type = forms.ChoiceField(choices=types_of_businesses, required=False, widget=forms.RadioSelect, label="Type Of Business")
  employer_name = forms.CharField(label="Employer name")
  CAC_no = forms.IntegerField(label="CAC Registration Number")
  CAC_reg_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
  address = forms.CharField(label="Address",required=False)
  house_no = forms.CharField(label="House No",required=False)
  street = forms.CharField(label="Street",required=False)
  postal_address=forms.CharField(label="Postal Address",required=False)
  Telephone1 = forms.IntegerField(label="Telephone1",required=False)
  Telephone2 = forms.IntegerField(label="Telephone2",required=False)

  class Meta:
    model = Employers
    fields = ['CAC_no','business_type','employer_name','CAC_reg_date','email','address','house_no','district','street',\
    'state','local_council','region','branch','postal_address','Telephone1','Telephone2',]

