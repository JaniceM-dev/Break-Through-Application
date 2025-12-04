from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate , login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render (request, 'Donor/home.html')

@login_required(login_url='login')
def userHome(request):
    context = {}
    return render (request , 'Donor/userhome.html' , context)
   
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except: 
            print("User Does Not Exist.")   
        
        user= authenticate(request, username=username , password=password)

        if user is not None:
           login(request, user)
           return redirect ('userHome')
        else:
         print("Wrong Details!!!!")

    context = {}
    return render (request, 'Donor/login.html' , context)    

def logoutUser(request):
    return render (request, 'Donor/logout.html')

def logingout( request):
    logout (request)
    return redirect ('Donorhome')

def registerUser (request):
    form = UserCreationForm

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save() 
            login(request, user)
            return redirect ('userHome')
    context = {"form": form}   

    return render (request, 'Donor/registerUser.html', context) 




   
    
# Create your views here.
