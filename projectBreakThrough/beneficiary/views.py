from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate , login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import AppealForm , MessageForm ,CustomRegistrationForm
from .models import Appeal , Message , Profile
from django.http import Http404
from .decorators import role_required
from django.db import IntegrityError

# Create your views here.
def home(request):
    return render (request, 'beneficiary/home.html')


@login_required(login_url='beneficiarylogin')
@role_required('beneficiary')
def userHome(request):
    context = {}
    return render (request , 'beneficiary/userhome.html' , context)
   
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user= authenticate(request, username=username , password=password)


        if user is not None:
           login(request, user)

           if user.is_superuser:
            return redirect('admin:index')
    
           
           try:
              role = user.profile.role
           except Profile.DoesNotExist:
               role = None

           if role == 'beneficiary':
               return redirect('beneficiaryuserHome')
           elif role == 'donor':
               return redirect('DonoruserHome')
           elif role == 'ngo':
               return redirect('NGOuserHome')
           
        else:
            print("Wrong Details!!!!")
          
    context = {}
    return render (request, 'beneficiary/login.html' , context)    

def logoutUser(request):
    return render (request, 'beneficiary/logout.html')

def logingout( request):
    logout (request)
    return redirect ('beneficiaryhome')

def registerUser (request):
    form = CustomRegistrationForm()

    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save() 
                role = form.cleaned_data.get('role')
                Profile.objects.create(user=user, role=role)
                login(request, user)

            except IntegrityError:
                form.add_error('username', 'This username is already taken.')
        
            if role == 'beneficiary':
              return redirect('beneficiaryuserHome')
            elif role == 'donor':
              return redirect('donorPendingApproval')
            elif role == 'ngo':
               return redirect('NGOuserHome')
    else:
        form = CustomRegistrationForm()

    context = {"form": form}   

    return render (request, 'beneficiary/registerUser.html', context) 

def makeRequest(request):
    form = AppealForm()

    if request.method == 'POST':
        form = AppealForm(request.POST)
        if form.is_valid():
            appeal = form.save(commit=False)  
            appeal.user = request.user        
            appeal.save()                     
            return redirect('beneficiaryreadRequests')
    
    context = {'form': form}
    return render(request, 'beneficiary/makeRequest.html', context)

from django.contrib.auth.decorators import login_required

@login_required(login_url='beneficiarylogin')
def readRequests(request):
    appeals = Appeal.objects.filter(user=request.user)  
    context = {'appeals': appeals}
    return render(request, 'beneficiary/requests.html', context)

@login_required(login_url='beneficiarylogin')
def readOneRequest(request, pk):
    try:
        appeal = Appeal.objects.get(id=pk, user=request.user)  
    except Appeal.DoesNotExist:
        return redirect('beneficiaryreadRequests') 

    context = {'appeal': appeal}
    return render(request, 'beneficiary/request.html', context)


@login_required(login_url='beneficiarylogin')
def updateRequest(request , pk):
    try:
        appeal = Appeal.objects.get(id=pk, user=request.user)
    except Appeal.DoesNotExist:
        raise Http404("You are not allowed to edit this request")
    form= AppealForm(instance= appeal)

    if request.method == 'POST':
        form = AppealForm (request.POST, instance=appeal)
        if form.is_valid():
            form.save()
            return redirect ('readRequests')
    context = {'form': form}
    return render (request, 'beneficiary/updateRequest.html' , context)

@login_required(login_url='beneficiarylogin')
def deleteRequest (request , pk):
    try:
        appeal = Appeal.objects.get(id=pk, user=request.user)
    except Appeal.DoesNotExist:
        raise Http404("You are not allowed to delete this request")

    if request.method == "POST":
       appeal.delete() 
       return redirect ('beneficiaryreadRequests')
    context = {'appeal':appeal}
    return render ( request ,'beneficiary/deleteRequest.html' ,context)

@login_required(login_url='beneficiarylogin')    
def contactUs(request):
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)  
            message.user = request.user    

            try:
                message.role = request.user.profile.role
            except Profile.DoesNotExist:
                message.role = 'unknown'

                
            message.save()                     
            return redirect('beneficiaryuserHome')
    
    context = {'form': form}
    return render(request, 'beneficiary/contactUs.html', context)

def aboutUs(request):
    return render (request, 'beneficiary/AboutUs.html')
