from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm,GithubUsersForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
import json
import requests
# Create your views here.
def index(request):
    return render(request,"basic_app/index.html")

@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered=False
    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user
            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            profile.save()
            registered=True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form=UserForm()
        profile_form=UserProfileInfoForm()
    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered,})



def user_login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'basic_app/login.html',{})

@login_required
def git_user_search(request):
    if request.method=="POST":
        git_username_form=GithubUsersForm(data=request.POST)
        if git_username_form.is_valid():
            git_user=git_username_form.save()
            url_1=requests.get("https://api.github.com/users/{}".format(git_user))
            url_2=requests.get("https://api.github.com/users/{}/repos".format(git_user))
            json_obect_1=url_1.json()
            json_object_2=url_2.json()
            r=json.dumps(json_object_2[0]["name"],indent=4,sort_keys=True)
            if r=='null':
                return HttpResponse("it does not exists")
            else:
                
                public_repos=json_obect_1["public_repos"]
                name_user=json_object_2[0]["owner"]["login"]
                name_project=json_object_2[0]["name"]
                lang_user=json_object_2[0]["language"]
                repo_user="https://github.com/"+json_object_2[0]["full_name"]
                return render(request,'basic_app/user_info.html',{"name_project":name_project,
                                                                  "lang_user":lang_user,
                                                                  "repo_user":repo_user,
                                                                  "name_user":name_user,
                                                                  "public_repos":public_repos,})
        else:
            return HttpResponse("kuch bhi matlab")
    else:
        return render(request,'basic_app/search_user.html',{"git_username_form":GithubUsersForm()})
