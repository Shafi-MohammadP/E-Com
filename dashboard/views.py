from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
# from categories.models import category

from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout

# verification email
from user.models import UserOTP
from user.views import validateemail,validatepassword
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError


def admin_signup(request):
    
    if request.method == 'POST':
        
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            user=User.objects.get(email=get_email)

            if int(get_otp)==UserOTP.objects.filter(user=user).last().otp:
                user.is_active=True
                user.save()
                auth.login(request,user)
                # messages.success(request,f'Account is created for {user.email}')
                UserOTP.objects.filter(user=user).delete()
                return redirect('usermanagement_1')
            else:
                messages.warning(request,f'you Entered a Wrong OTP')
                return render(request,'dashboard/admin_signup.html',{'otp':True,'user':user})
        else:
            username=request.POST['username']
            email=request.POST['email']
            password1=request.POST['password1']
           
            
            context={
                    'pre_username':username,
                    'pre_email':email,
                    'pre_password1':password1,     
            }
            
            if username.strip()=='' or password1.strip()=='' or email.strip()=='' :
                messages.error(request,'field cannot empty!')
                return render(request,'dashboard/admin_signup.html',context )
            
            elif User.objects.filter(username=username):
                messages.error(request,'username alredy exist!')
                context['pre_username']=''
                return render(request,'dashboard/admin_signup.html',context )
            
            elif not re.match(r'^[a-zA-Z\s]*$',username):
                messages.error(request,'Username should only contain alphabets!')  
                context['pre_username']=''
                return render(request,'dashboard/admin_signup.html',context )
                
            elif User.objects.filter(email=email):
                messages.error(request,'email already exist!')
                context['pre_email']=''
                return render(request,'dashboard/admin_signup.html',context ) 
    
            email_check=validateemail(email)
            if email_check is False:
                messages.error(request,'email not valid!')
                context['pre_email']=''
                return render(request,'dashboard/admin_signup.html',context )
            
            password_check=validatepassword(password1)
            if password_check is False:
                messages.error(request,'Enter strong password!')
                context['pre_password1']=''
                return render(request,'dashboard/admin_signup.html',context)
            
            user=User.objects.create_user(username=username,email=email,password=password1)
            user.is_active=False
            user.is_superuser=True
            user.save()
            user_otp=random.randint(100000,999999)
            UserOTP.objects.create(user=user,otp=user_otp)
            mess=f'Hello \t{user.username},\nYour OTP to verify your account for MS Sounds is {user_otp}\n Thanks You!'
            send_mail(
                "Welcome to MS Sounds , verify your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],

                fail_silently=False
                )
            return render(request,'dashboard/admin_signup.html',{'otp':True,'user':user})  
        
    return render(request,'dashboard/admin_signup.html')
    
def usermanagement_1(request):
    return render(request,'dashboard/dashboardbase.html')
    
    # return render(request,'dashboard/usermanagement.html')
def admin_login1(request):
    # if request.user.is_authenticated:
    #     return redirect('home')#dashboard user
   
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        
        
        if username.strip()=='' or password.strip()=='':
            messages.error(request,'field cannot empty!')
            return redirect('admin_login1')
    
        user=authenticate(username=username,password=password)
        
        if user is not None:
            
            if user.is_active:
                if user.is_superuser:
                    login(request,user)
                    return redirect('dashboardog') #dashboard user
                else:
                    messages.warning(request,'your not admin!')
                return redirect('admin_login1')
                    
            else:
                messages.warning(request,'your account has been blocked!')
                return redirect('admin_login1')
            
        else:
            messages.error(request,'invalid username or password!')
            return redirect('admin_login1')
    
    return render(request,'dashboard/admin_login1.html') 
@login_required(login_url='admin_login1')   
def dashboard(request):
    return render(request,'dashboard/dashboardbase.html')

@login_required(login_url='admin_login1')
def dashboardog(request):
    return render(request,'dashboard/dash.html')
def admin_forgotpassword(request):
    if request.method=='POST':
        get_email=request.POST.get('email') 
        user=User.objects.filter(email=get_email).first()
        if not user:
            messages.error(request,'email does not exist!')
            return render(request,'dashboard/password_admin_forgot.html')
        if user.is_superuser:
            get_otp=request.POST.get('otp')
            if get_otp:
                get_email=request.POST.get('email') 
                user=User.objects.get(email=get_email)
                if int(get_otp)==UserOTP.objects.filter(user=user).last().otp:
                    password1 = request.POST.get('password1')
                    password2 = request.POST.get('password2')
                    context ={
                                    'pre_otp':get_otp,
                                }
                    if password1.strip()==''or password2.strip()=='':
                        messages.error(request,'field cannot empty !')
                        return render(request,'dashboard/password_admin_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                    
                    elif password1 != password2:
                        messages.error(request,'Password does not match!')
                        return render(request,'dashboard/password_admin_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                        
                    Pass = validatepassword(password1)
                    if Pass is False:
                        messages.error(request,'Please enter Strong password!')
                        return render(request,'dashboard/password_admin_forgot.html',{'otp':True,'user':user,'pre_otp':get_otp})
                    user.set_password(password1)
                    user.save()
                    UserOTP.objects.filter(user=user).delete()
                    messages.success(request,'Your password is changed!')
                    return redirect('admin_login1')
                else:
                    messages.warning(request,'You Entered a wrong OTP!')
                    return render(request,'dashboard/password_admin_forgot.html',{'otp':True,'user':user})  
            else:
                email=request.POST['email']
                
                if email.strip()=='':
                    messages.error(request,'field cannot empty!')
                    return render(request,'dashboard/password_admin_forgot.html')
                
                email_check=validateemail(email)
                if email_check is False:
                    messages.error(request,'email not valid!')
                    return render(request,'dashboard/password_admin_forgot.html')
            
                if User.objects.filter(email=email):
                    user=User.objects.get(email=email)
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=user,otp=user_otp)
                    message=f'Hello\t{user.username},\n Your OTP to verify your account for MS Sounds is {user_otp}\n Thanks' 
                    send_mail(
                        "welcome to MS Sounds Verify Email",
                        message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    return render (request,'dashboard/password_admin_forgot.html',{'otp':True,'user':user}) 
                else:
                    messages.error(request,'email does not exist!')
                    return render(request,'dashboard/password_admin_forgot.html')
        else:
             messages.error(request,'you are not admin!')
             return render(request,'dashboard/password_admin_forgot.html')
                    
    return render (request,'dashboard/password_admin_forgot.html')
@login_required(login_url='admin_login1')
def admin_logout1(request):
    logout(request)
    return redirect('admin_login1')


@login_required(login_url='admin_login1')
def users_listing(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    user_data = User.objects.all().order_by('id')
    return render(request,'dashboard/usermanagement.html',{'users':user_data})

@login_required(login_url='admin_login1')   
def blockuser(request,user_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('users_listing')




    
