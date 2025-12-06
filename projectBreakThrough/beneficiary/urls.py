from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name = 'beneficiaryhome'),
    path('login' , views.loginUser , name ='beneficiarylogin'),
    path('userHome' , views.userHome , name ='beneficiaryuserHome'),
    path('logout' , views.logoutUser , name = 'beneficiarylogout'),
    path('logingout' , views.logingout , name = 'beneficiarylogingout'),
    path('register' , views.registerUser , name = 'beneficiaryregister'),
    path('makeRequest' , views.makeRequest , name = 'beneficiarymakeRequest') ,
    path('Requests' , views.readRequests , name = 'beneficiaryreadRequests') ,
    path('MyRequest/<str:pk>' , views.readOneRequest , name = 'beneficiaryreadOneRequest'),
    path('updateRequest/<str:pk>' , views.updateRequest , name = 'beneficiaryupdateRequest') ,
    path('deleteRequest/<str:pk>' , views.deleteRequest , name = 'beneficiarydeleteRequest') ,
    path('contactUs' , views.contactUs , name = 'beneficiarycontactUs') 
]