from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name = 'NGOhome'),
    path('login' , views.loginUser , name ='NGOlogin'),
    path('userHome' , views.userHome , name ='NGOuserHome'),
    path('logout' , views.logoutUser , name = 'NGOlogout'),
    path('logingout' , views.logingout , name = 'NGOlogingout'),
    path('register' , views.registerUser , name = 'NGOregister'),
    path('contactUs' , views.contactUs , name = 'NGOcontactUs') ,
    path('viewRequests' , views.viewRequests , name = 'NGOviewRequests') ,
    path('viewDonations' , views.viewDonations , name = 'NGOviewDonations') ,
    path('viewOneRequest/<str:pk>' , views.viewOneRequest, name = 'NGOviewOneRequest') ,
    path('viewDonors', views.viewDonors, name = 'NGOviewDonors'),
    path('viewDonor/<str:pk>' , views.viewDonor, name = 'NGOviewDonor'),
    path('authorizeRequest/<str:pk>' , views.authorizeRequest, name = 'NGOauthorizeRequest'),
    path('authorizeDonor/<str:pk>' , views.authorizeDonor, name = 'NGOauthorizeDonor'),
    path('aboutUs' , views.aboutUs , name = 'NGOaboutUs')
]