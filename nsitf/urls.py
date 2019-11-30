from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('registeremployer',views.EmployerFormView.as_view(), name = 'reg_employer'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('submitnewemployer/', views.submit_new_employer,name='submitnewemployer'),
    path('registrationsuccess/', views.registration_success,name='registrationsuccess'),
    path('chaining/', include('smart_selects.urls')),
   
    
]
