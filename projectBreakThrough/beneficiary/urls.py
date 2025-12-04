from django.urls import path
from . import views

urlpatterns = [
    path('' , views.home , name = 'beneficiaryhome'),
    path('login' , views.loginUser , name ='login'),
    path('userHome' , views.userHome , name ='userHome'),
    path('logout' , views.logoutUser , name = 'logout'),
    path('logingout' , views.logingout , name = 'logingout'),
    path('register' , views.registerUser , name = 'register') 
]