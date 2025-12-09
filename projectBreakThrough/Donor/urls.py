from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name = 'Donorhome'),
    path('login' , views.loginUser , name ='Donorlogin'),
    path('userHome' , views.userHome , name ='DonoruserHome'),
    path('logout' , views.logoutUser , name = 'Donorlogout'),
    path('logingout' , views.logingout , name = 'Donorlogingout'),
    path('register' , views.registerUser , name = 'Donorregister'),
    path('index' , views.index , name = 'index'),
    path('mpesaPayement/<str:pk>' , views.mpesaPayement , name = 'mpesaPayement'),
    path('viewRequests' , views.viewRequests , name = 'DonorviewRequests'),
    path('viewOneRequest/<str:pk>' , views.viewOneRequest , name = 'DonorviewOneRequest'),
    path('contactUs' , views.contactUs , name = 'DonorcontactUs') ,
    path('donorDonationHistory' , views.donorDonationHistory , name = 'donorDonationHistory') ,
    path('donorPendingApproval' , views.donorPendingApproval , name = 'donorPendingApproval'), 
    path('aboutUs' , views.aboutUs , name = 'donoraboutUs') 
]
    