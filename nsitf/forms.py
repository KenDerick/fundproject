from django import forms
from nsitf.models import (Employers,Employees,State,Branches,Regions,Local_Government)
from bootstrap_datepicker_plus import DatePickerInput

class EmployerRegForm(forms.ModelForm):
    name = forms.CharField(label='Enter Employer Name')
    class Meta():
        model = Employers
        fields = '__all__'


class EmployerRegistrationForm(forms.ModelForm):
    CAC_reg_date = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'))
    #     widget=DatePickerInput(format='%d/%m/%Y')
    # )

    # date_registered = forms.DateField(label="Pick Your Intended Leave Date")
    # date_registered.widget.attrs['readonly'] = False
    # widgets = {'date_registered': forms.DateInput(attrs={'class': 'datepicker'})}
    CAC_no = forms.IntegerField(label="Enter CAC Registration Number")
    address1 = forms.CharField(label="Enter Employer Address")
    house_no = forms.CharField(label="Enter Employer House No")
    street = forms.CharField(label="Enter Employer street")
    # branch = forms.ModelChoiceField(queryset=Branches.objects.all(),label="Select Employer Branch")
    name = forms.CharField(label="Enter Employer name")
    
    # leave_docs =forms.FileField(label="Please Attach Documents For Leave",required=False)
    class Meta:
        model = Employers
        fields = ['CAC_reg_date','CAC_no','address1','house_no','street','name','state',\
        'local_council','region','branch',]


        
