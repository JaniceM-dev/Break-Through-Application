from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate , login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from beneficiary.models import Appeal , Profile , Message
from beneficiary.forms import AppealForm , CustomRegistrationForm ,MessageForm
from Donor.models import Donation
from django.http import HttpResponseForbidden , Http404
from beneficiary.decorators import role_required 
from django.db.models import Count
from django.db import IntegrityError
# Create your views here.
def home(request):
    return render (request, 'NGO/home.html')

@login_required(login_url='NGOlogin')
@role_required('ngo')
def userHome(request):
    context = {}
    return render (request , 'NGO/userhome.html' , context)
   
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
                return HttpResponseForbidden("Profile not found.")

            if role == 'ngo':
                return redirect('NGOuserHome')
            else:
                return HttpResponseForbidden("You are not allowed to access the NGO app.")
        else:
            print("Wrong Details!!!!")
    context = {}
    return render (request, 'NGO/login.html' , context)    

def logoutUser(request):
    return render (request, 'NGO/logout.html')

def logingout( request):
    logout (request)
    return redirect ('NGOhome')

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

    return render (request, 'NGO/registerUser.html', context) 

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
            return redirect('NGOuserHome')
    
    context = {"form": form}   
    return render (request, 'NGO/contactUs.html', context)

def viewRequests(request):
    appeals = Appeal.objects.filter(user__profile__role='beneficiary')
    donations = Donation.objects.select_related('appeal', 'user').all()
    context = {'appeals': appeals , 'donations': donations}
    return render(request, 'NGO/requests.html', context)

def viewOneRequest(request , pk):
    appeal = Appeal.objects.get(id=pk)
    donations = Donation.objects.filter(appeal=appeal)
    context = {'appeal': appeal , 'donations': donations}
    return render (request, 'NGO/request.html' , context)

def viewDonations(request):
    donations = Donation.objects.select_related('appeal', 'user').all()
    context = { 'donations': donations }
    return render(request, 'NGO/donations.html' ,context) 

def viewDonors(request):
    donors = User.objects.filter(profile__role='donor').annotate(num_donations=Count('donation'))
    context = {'donors': donors}
    return render (request, 'NGO/donors.html' , context)
# Create your views here.

@login_required(login_url='NGOlogin')
@role_required('ngo')
def authorizeRequest(request, pk):
    appeal = Appeal.objects.get(id=pk)
    appeal.is_authorized = True
    appeal.status = 'authorized' 
    appeal.save()
    return redirect('NGOviewRequests')

 
def viewDonor(request , pk):
    donor =User.objects.get(id=pk)
    context = {'donor': donor}
    return render(request, 'NGO/donor.html', context )
   
@login_required (login_url='NGOlogin')
@role_required('ngo')
def authorizeDonor(request,pk):
    donor = User.objects.get(id=pk)
    donor.profile.is_authorized = True
    donor.profile.save()
    return redirect('NGOviewDonors')

def aboutUs(request):
    return render (request, 'NGO/aboutUs.html')

