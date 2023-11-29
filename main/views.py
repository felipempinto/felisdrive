from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages 
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes, force_str#force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.db.models import Case, Value, When, F
from django.db import models

from .forms import NewUserForm
from .token import account_activation_token
from .models import APIToken,Folder,Data

import pytz
import datetime
import os
import jwt

SECRET_KEY_TOKEN = os.environ.get("SECRET_KEY")

def homepage(request):
    # samples = Data.objects.order_by('-created_at')[:3]
    folder = Folder.objects.get(name="/")
    datasets = Data.objects.filter(folder=folder)
    #TODO:
    # Select only folders without "/" in the name
    folders = Folder.objects.all()

    return render(request,
                  template_name='main/homepage.html',
                  context={
                      "folders":folders,
                      "datasets":datasets,
                      "folder":folder,
                      }
                  )


def folder_detail(request, slug):
    folder = get_object_or_404(Folder, slug=slug)
    datasets = Data.objects.filter(folder=folder)
    #TODO:
    # Select folders that starts with the folder name
    # folders = Folder.objects.all()

    return render(request, 'main/homepage.html', {
        # "folders":folders,
        "datasets":datasets,
        "folder":folder,

        })


def pages(request,folder):
    folder = Folder.objects.get(folder)
    datasets = Data.objects.filter(folder=folder)



# @login_required(login_url='/login/')
def upload(request,folder):#,source):

    if request.method == 'POST':
        if folder=="home":
            folder='/'
        folder = Folder.objects.get(name=folder)
        # uploaded_file = request.FILES[f'file']
        # dataset = Data(file=uploaded_file,folder=folder)
        # dataset.save()

        # uploaded_file = request.FILES[f'file']
        files = request.FILES.getlist('file')
        for file in files:
            print(file)
            dataset = Data(file=file,folder=folder)
            dataset.save()

    return redirect('main:homepage')


def about(request):

    return render(request,
                  template_name='main/about.html',
                  context={   
                           
                           }
                  )

def logout_request(request):
    logout(request)
    messages.info(request,"You are logged out")
    return redirect("main:homepage")

def login_request(request):
    if request.user.is_authenticated:
        return redirect("main:user")
    else:
        if request.method == "POST":
            form = AuthenticationForm(request,data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username = username,password = password)
                if user is not None:
                    login(request, user)
                    messages.info(request, f"You are logged as {username}")
                    return redirect("main:homepage")
                else:
                    messages.error(request,"Username or password don't match")
            else:
                messages.error(request,"Username or password don't match")
        form = AuthenticationForm()
        return render(request,
                    "main/login.html",
                    {"form":form})

def activate(request, uidb64, token):
    try:
        # uid = force_text(urlsafe_base64_decode(uidb64))
        uid = force_str(urlsafe_base64_decode(uidb64))
        
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.info(request, f"You are logged as {user.username}")
        return redirect("main:homepage")
    else:
        return HttpResponse('Activation link is invalid!')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST) 
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            user_email = User.objects.filter(email=to_email)
            if len(user_email)>0:
                messages.error(request, "The email you are trying to use, is already being used.")
                form = NewUserForm
                return render(request = request,
                              template_name = "main/register.html",
                              context={"form":form})

            # user = form.save()
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            tk = account_activation_token.make_token(user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your DeepForest account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':tk,
            })
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, 'Please confirm your email address to complete the registration')
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})
    form = NewUserForm
    return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form})

@login_required
def user_page(request):
    user = request.user
    api_tokens = APIToken.objects.filter(user=user)
    if request.method == 'POST':
        tzname = request.COOKIES.get("django_timezone")
        date = request.POST.get('expires_in_hours')
        if tzname:
            tz = pytz.timezone(tzname)
            date = tz.localize(datetime.datetime.strptime(date, '%Y-%m-%d'))
        else:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        
        expires_at = int((date).timestamp())
        
        api_token = jwt.encode({'email': user.email, 'exp': expires_at},  SECRET_KEY_TOKEN, algorithm='HS256')
        APIToken.objects.create(user=user, token=api_token, expires_at=datetime.datetime.fromtimestamp(expires_at, tz))
        return redirect('main:user_page')
    return render(request, 'main/user_page.html', {'user': user, 'api_tokens': api_tokens})

def delete_token(request,pk):
    api_token = APIToken.objects.get(id=pk)
    if api_token.user != request.user:
        messages.error(request, "You don't have permission to delete this token")
        return redirect("user_page")
    api_token.delete()
    messages.success(request, "Token deleted successfully")
    return redirect('main:user_page')



