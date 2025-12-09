from django.shortcuts import render , redirect 
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate , login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from .models import Donation
from beneficiary.models import Appeal , Profile, Message
from beneficiary.forms import AppealForm , CustomRegistrationForm ,MessageForm
from django.http import HttpResponseForbidden , Http404
from beneficiary.decorators import role_required 
from django.db import IntegrityError
# Create your views here.
def home(request):
    return render (request, 'Donor/home.html')


@login_required(login_url='Donorlogin')
@role_required('donor')
def userHome(request):
    context = {}
    return render (request , 'Donor/userhome.html' , context)
   
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin:index')

            try:
                role = user.profile.role
            except Profile.DoesNotExist:
                return HttpResponse("Profile not found.")

            if role == 'donor':
                if user.profile.is_authorized:
                    return redirect('DonoruserHome')
                else:
                  return redirect('donorPendingApproval')
            else:
                return HttpResponseForbidden("You are not allowed to access the Donor app.")
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

    return render (request, 'Donor/registerUser.html', context) 


def index(request):
    # cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    # phone_number = '0116960694'
    # amount = 1
    # account_reference = 'reference'
    # transaction_desc = 'Description'
    # callback_url = 'https://api.darajambili.com/express-payment'
    # response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def mpesaPayement( request , id = None , pk = None):
    cl = MpesaClient()
    accountReference = 'BREAKTHROUGH ORGANIZATION'
    transactionDesc = 'Donation To a Request'
    callbackUrl = 'https://api.darajambili.com/express-payment'
    appeal = None
    if pk:
        appeal = Appeal.objects.get(id=pk)


    if request.method == "POST":
        phoneNumber = request.POST.get ('phoneNumber')
        amount = int( float (request.POST.get ('amount')))

        response = cl.stk_push(phoneNumber, amount, accountReference, transactionDesc, callbackUrl)

        if appeal:
            Donation.objects.create(
                user=request.user,
                appeal=appeal,
                amount=amount,
            )
         
            appeal.status = 'donated'
            appeal.save()
            return redirect ('donorDonationHistory')

        context = {"response" : response ,'appeal': appeal}
        return render (request, 'Donor/paymentsMpesa.html' , context)
    else :
         
         return render (request, 'Donor/paymentsMpesa.html' ,{'appeal': appeal})
    
    
# Create your views here.
def viewRequests(request):
    appeals = Appeal.objects.filter(user__profile__role='beneficiary')
    context = {'appeals': appeals}
    return render (request, 'Donor/requests.html' , context)

def viewOneRequest(request , pk):
    appeal = Appeal.objects.get(id=pk)
    context = {'appeal': appeal}
    return render (request, 'Donor/request.html' , context)

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
            return redirect('DonoruserHome')
    
    context = {'form': form}
    return render(request, 'Donor/contactUs.html', context)

@login_required(login_url='Donorlogin')
@role_required('donor')

def donorDonationHistory(request):
    donations = Donation.objects.filter(user=request.user)
    context = {'donations': donations}
    return render(request, 'Donor/donations.html', context)

@login_required(login_url='Donorlogin')
@role_required('donor')
def donorPendingApproval(request):
    return render(request, 'Donor/waitingApproval.html')

def aboutUs (request):
    return render (request ,'Donor/aboutUs.html' )