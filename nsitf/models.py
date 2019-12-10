import os
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager,Group
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
now = timezone.now()
from smart_selects.db_fields import ChainedForeignKey

class Regions(models.Model):
    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, unique=False)

    def __str__(self):
        return self.name


class Branches(models.Model):
    region = models.ForeignKey(Regions,models.SET_NULL,blank=True, null=True,unique=False)
    name = models.CharField(max_length=100,blank=True,null=True)
    

    def __str__(self):
        return self.name


class State(models.Model):
    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50,blank=True, null=True,unique=False)

    def __str__(self):
        return self.name


class Local_Government(models.Model):
    state = models.ForeignKey(State,on_delete=models.SET_NULL,blank=True, null=True,unique=False)
    name =  models.CharField(max_length=50,blank=True, null=True,unique=False)
    # state = models.PositiveIntegerField( blank=True, null=True, unique=False)

    def __str__(self):
        return self.name


class City(models.Model):
    state = models.ForeignKey(State, models.SET_NULL, blank=True, null=True, unique=False)
    name = models.CharField(max_length=50, blank=True, null=True, unique=False)

    def __str__(self):
        return self.name     

class AllStaff(models.Model):
    staff_id = models.PositiveIntegerField(unique=True,primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50)
    display_name=models.CharField(max_length=250,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True,unique=False)
    region = models.ForeignKey(Regions,on_delete=models.SET_NULL, null=True,)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branches,models.SET_NULL,blank=True,null=True,unique=False)
    is_Entry_staff = models.BooleanField(default=False)
    is_Approval_manager = models.BooleanField(default=False)
    is_Sys_admin = models.BooleanField(default=False)
    # queue_code = models.IntegerField(unique=False,default=0)
    #queue_code = models.ForeignKey(LeaveTaskQueue,models.CASCADE,unique=False,blank=True,null=False,default=11)
    #rank = models.ForeignKey(Rank,models.SET_NULL,blank=True,null=True,unique=False)
   


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def create_user(self, email, staff_id,password):
        user = self.model(email=email, staff_id=staff_id, password=password)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = False
        user.last_login = now
        user.save(using=self._db)
        return user

    def create_superuser(self, email, staff_id, password):
            user = self.create_user(email=email, staff_id=staff_id, password=password)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.last_login = now
            user.save(using=self._db)
            return user


class User(AbstractUser):
    """User model."""
    staff_id = models.PositiveIntegerField(unique=True,primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50)
    middle_name=models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50)
    display_name=models.CharField(max_length=250,blank=True,null=True)
    phone = models.CharField(max_length=15,blank=True,null=True,unique=False)
    username = None
    region = models.ForeignKey(Regions,on_delete=models.SET_NULL, null=True,)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branches,models.SET_NULL,blank=True,null=True,unique=False)
    is_Entry_staff = models.BooleanField(default=False)
    is_Approval_manager = models.BooleanField(default=False)
    is_Sys_admin = models.BooleanField(default=False)
    # queue_code = models.IntegerField(unique=False,default=0)
    #queue_code = models.ForeignKey(LeaveTaskQueue,models.CASCADE,unique=False,blank=True,null=False,default=11)
    #rank = models.ForeignKey(Rank,models.SET_NULL,blank=True,null=True,unique=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['staff_id',]
    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.display_name
    #     # return user.display_name

    def get_staff_id(self):
        ''' Returns the staff_id '''
        return self.staff_id

    def get_full_name(self):
        ''' Returns the first_name plus the last_name, with a space in between. '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        ''' Returns the short name for the user. '''
        return self.first_name


class Registration_Status(models.Model):
    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True, unique=False)

    def __str__(self):
        return self.name



class Employers(models.Model):
    employer_code=models.AutoField(primary_key=True,unique=True)
    employer_name = models.CharField(max_length=150)
    CAC_no = models.IntegerField(blank=True,null=True,unique=False)
    CAC_reg_date = models.DateField(blank=True,null=True)
    address=models.CharField(max_length=150,blank=True,null=True)
    house_no=models.CharField(max_length=150,blank=True,null=True)
    street=models.CharField(max_length=150,blank=True,null=True)
    district=models.CharField(max_length=50,blank=True,null=True)
    state=models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    local_council = ChainedForeignKey(
        Local_Government,
        chained_field="state",
        chained_model_field="state",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True)
    postal_address=models.CharField(max_length=150,blank=True,null=True)
    Telephone1 = models.IntegerField(blank=True,null=True) 
    Telephone2 = models.IntegerField(blank=True,null=True)
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)
    submitted_by = models.ForeignKey(User,models.SET_NULL,blank=True,null=True,unique=False, related_name='submitted_by')
    submitted_on = models.DateTimeField(auto_now_add=True,blank=True, null=True,unique=False)
    notes = models.TextField(blank=True, null=True)
    region = models.ForeignKey(Regions, on_delete=models.SET_NULL,blank=True,null=True,unique=False)
    branch = ChainedForeignKey(
        Branches,
        chained_field="region",
        chained_model_field="region",
        show_all=False,
        auto_choose=True,
        sort=True)
    certificate_no = models.IntegerField(blank=True, null=True, unique=False)
    status = models.ForeignKey(Registration_Status, on_delete=models.SET_NULL, null=True, default='1')
    business_type = models.CharField(max_length=100,blank=True, null=True)
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='changed_by')
    last_changed_on = models.DateTimeField(auto_now_add=True,blank=True, null=True,unique=False)
    # queue_code = models.ForeignKey(Reg_Task_Queue, models.SET_NULL, null=True, unique=False)
    # ECS_no = models.IntegerField(blank=True, null=True, unique=False)

    
    def __str__(self):
        return self.employer_name


class Employees(models.Model):
    employee_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # employer = models.ForeignKey(Employers, on_delete=models.CASCADE, related_name='emplyees')

    def __str__(self):
        return (self.first_name+' '+self.last_name+'--'+self.employee_id)

class CAC_DB(models.Model):
    cac_no = models.IntegerField()
    company_name = models.CharField(max_length=100)
    address=models.CharField(max_length=150)
    Reg_date = models.DateField()


class Reg_Task_Queue(models.Model):
   code = models.AutoField(primary_key=True, unique=True)
   name = models.CharField(max_length=150,null=True,blank=True)


class Reg_Task_Route(models.Model):
    branch=models.OneToOneField(Branches, on_delete=models.CASCADE, primary_key=True)
    approval_queue = models.ForeignKey(
        Reg_Task_Queue, models.SET_NULL, blank=True, null=True, unique=False, related_name='approvalqueue')


class Reg_Tasks(models.Model):
    code = models.OneToOneField(Employers, on_delete=models.CASCADE, primary_key=True)
    queue_code =  models.ForeignKey(Reg_Task_Queue, models.SET_NULL, blank=True, null=True, unique=False, related_name='tasks_queue')
    name = models.CharField(max_length=200, null=True, blank=True)
    CAC_no = models.IntegerField(blank=True, null=True, unique=False)
    CAC_reg_date = models.DateField(blank=True, null=True)
    sent_by = models.ForeignKey( User, models.SET_NULL, blank=True, null=True, unique=False)
    sent_on = models.DateTimeField(blank=True, null=True, unique=False)
    branch = models.ForeignKey(Branches, models.SET_NULL, blank=True, null=True, unique=False, related_name='taskbranch')
    status = models.ForeignKey(Registration_Status, on_delete=models.SET_NULL, null=True)