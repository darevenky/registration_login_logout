from django.shortcuts import render

# Create your views here.

from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        UFO=UserForm(request.POST)
        PFO=ProfileForm(request.POST,request.FILES)

        if UFO.is_valid() and PFO.is_valid():
            USUO=UFO.save(commit=False)
            password=UFO.cleaned_data['password']
            USUO.set_password(password)
            USUO.save()

            USPO=PFO.save(commit=False)
            USPO.username=USUO
            USPO.save()

            send_mail('Registratioon',
                      "Succefully Registration is Done",
                      'darevenky96@gmail.com',
                      [USUO.email],
                      fail_silently=False

                      )
            return HttpResponse('registration is succefull')
        else:
            return HttpResponse('not valid data')
    return render(request,'registration.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        AUO=authenticate(username=username,password=password)

        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('data not valid')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)
