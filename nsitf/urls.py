from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addnewuser/', views.addnewuser, name='addnewuser'),
    path('signup/', views.signup, name='signup'),
    path('submitnewemployer/', views.submit_new_employer, name='submitnewemployer'),
    path('partialsave1/', views.employerformone,name='partialformone'),
    path('partialsave2/<int:pk>', views.employerformtwo,name='partialformtwo'),
    path('upload-csv/<int:pk>', views.employee_upload, name='employee_upload'),
    path('chaining/', include('smart_selects.urls')),
    path('ajax/load-cac/', views.search_cac, name='ajax_load_cac'),
    path('detailsdashboard/', views.details_dashboard, name='details_dashboard'),
    path('cancelregistration/<int:pk>', views.cancel_registration, name='cancelregistration'),
    path('mycancelledregistrations/', views.cancelled_registrations, name='mycancelledregistrations'),
    path('editregistration/<int:pk>', views.edit_registration, name='editregistration'),
    path('sendtotaskqueue/<int:pk>',views.route_tasks,name='sendtotaskqueue'),
    path('taskqueue/', views.task_queues_view, name='taskqueueview'),
    path('taskdetailsview/<int:pk>', views.task_details_view,name='taskdetailsview'),
    path('returnregistration/<int:pk>', views.return_registration,name='returnregistration'),
    path('approveregistration/<int:pk>', views.approve_registration,name='approve_registration'),
    path('mailtemplate/', views.mail_template, name='mail_template'),
]
