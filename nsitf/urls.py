from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('registeremployer',views.EmployerFormView.as_view(), name = 'reg_employer'),
    path('submitnewemployer/', views.submit_new_employer, name='submitnewemployer'),
    path('chaining/', include('smart_selects.urls')),
    path('addnewuser/', views.addnewuser, name='addnewuser'),
    path('signup/', views.signup, name='signup'),
    path('ajax/load-cac/', views.search_cac, name='ajax_load_cac'),
    path('registrationdetails/', views.details_dashboard, name='reg_details'),
    path('cancelregistration/<int:pk>', views.cancel_registration, name='cancelregistration'),
    path('mycancelledregistrations/', views.cancelled_registrations, name='mycancelledregistrations'),
    # path('submitregistration/<int:pk>', views.submit_registration, name='submitregistration'),
    path('registrationsuccess/', views.registration_success, name='registrationsuccess'),
    path('sendtotaskqueue/<int:pk>',views.route_tasks,name='sendtotaskqueue'),
    path('taskqueue/', views.task_queues_view, name='taskqueueview'),
]
