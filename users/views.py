from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render,HttpResponse
from django.contrib import messages
from .forms import RegistrationForm, VerifyForm
from .utils import account_activation_token
from .models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text
import json
from twilio.rest import Client
import math, random

# Create your views here.
from django.conf import settings


account_sid = 'AC6ca36161db8b890f8763d35c7c8b3532'
auth_token = 'ac2fc1e94bab50e138349f1458243369'
client = Client(account_sid, auth_token)
# def send_verfication_code(country_code,phone_number):
#     data = {
#     'api_key': settings.AUTHY_KEY,
#     'via': 'sms',
#     'country_code': country_code,
#     'phone_number': phone_number,
#     }
#     url = 'https://api.authy.com/protected/json/phones/verification/start'
#     response = requests.post(url,data=data)
#     return response

# def verify_sent_code(one_time_password, user):
#     data= {
#     'api_key': settings.AUTHY_KEY,
#     'country_code': user.country_code,
#     'phone_number': user.phone_number,
#     'verification_code': one_time_password,
#     }

#     url = 'https://api.authy.com/protected/json/phones/verification/check'
#     response = requests.get(url,data=data)
#     return response

def home(request):
    return render(request,'users/home.html')
def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(request=request,data=request.POST)
        form.fields['username'].widget.attrs['class']='form-control'
        form.fields['password'].widget.attrs['class']='form-control'
        if form.is_valid():
            uname=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=uname,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return redirect('/login/')
        return render(request,'users/login.html',{'form':form})
    else:
        form=AuthenticationForm()
        form.fields['username'].widget.attrs['class']='form-control'
        form.fields['password'].widget.attrs['class']='form-control'
        return render(request, 'users/login.html',{'form':form})

def registration_view(request):
    if request.method=='GET':
        form=RegistrationForm()
    else:
        form=RegistrationForm(request.POST)
        if form.is_valid():
            
            user = form.save() 
            request.session['pk']=user.pk 
            
            
            otp=generateOTP()
            # print(otp)
            user.otp=otp
            user.save()
            phone_number=""+str(user.phone_number)
            
            
            # messages.success(request,'Congratulations!! Registered Succesfully')
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/activate.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'nasirkhan97.bd@gmail.com', [to_email])
            client.messages.create(
                to=phone_number, 
                from_="+12058289469",
                body="Hello from Python! ...your otp is "+otp)
            return redirect('verify')
            # client.verify \
            #         .services('VAefa2180efc938efb899b763e5561b2bb') \
            #         .verifications \
            #         .create(to=+8801627897267, channel='sms')
                   
            # request.method = 'GET'
            # return PhoneVerificationView({'user':user})
    return render(request,'users/registration.html',{'form':form})





def activate_user(request, uidb64, token):
    
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_verified=True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def activate_email(request, uid, token):
    
    
    pk=request.session.get('pk') 
    user=User.objects.get(pk=pk) 
    
    if user is not None:
        user.is_email_verified=True
        user.save()
        return redirect('activation/<uid>/<token>')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def verify_view(request):
    if request.method=='GET':
        form=VerifyForm()
    else:
        form=VerifyForm(request.POST)
        if form.is_valid():
            verification_code = request.POST['code'] 
            pk=request.session.get('pk') 
            user=User.objects.get(pk=pk)        
            if verification_code==user.otp:
               login(request, user)
               if user.is_phone_verified is False:
                   user.is_phone_verified = True
                   user.save()
               return redirect('/')
            else:
               messages.add_message(request, messages.ERROR,
                               'Verification Failled')
    return render(request, 'users/verify.html', {'form':form})

def generateOTP():
  digits = "0123456789"
  OTP = ""
#   print("OTP Generation")
  for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
  return OTP