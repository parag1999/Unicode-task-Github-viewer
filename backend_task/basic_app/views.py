from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm,GithubUsersForm,ContactForm
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
    found=False
    if request.method=="POST":
        git_username_form=GithubUsersForm(data=request.POST)
        if git_username_form.is_valid():
            github_user=git_username_form.save()
            url=requests.get("https://api.github.com/search/users?q={} in:fullname&per_page=100".format(github_user))
            #url_2=requests.get("https://api.github.com/users/{}/repos".format(github_user))
            json_object=url.json()
            count=json_object["total_count"]
            #json_object_2=url_2.json()

            #r=json.dumps(json_object_2[0]["name"],indent=4,sort_keys=True)
            #info=[]
            if count==0:
                found=True
                return render(request,'basic_app/search_user.html',{"git_username_form":GithubUsersForm(),"found":found})
            else:

                return render(request,'basic_app/user_list.html',{"user_search_list":json_object})

        else:
            return HttpResponse("INVALID FORM")
    else:
        return render(request,'basic_app/search_user.html',{"git_username_form":GithubUsersForm()})




@login_required
def git_user_info(request,user):
        url_1=requests.get("https://api.github.com/users/{username}".format(username=user))
        url_2=requests.get("https://api.github.com/users/{username}/repos".format(username=user))
        json_object_1=url_1.json()
        json_object_2=url_2.json()
        return render(request,'basic_app/user_info.html',{"user_info":json_object_1,"repo_info":json_object_2})



@login_required
def commit_info(request,user,repo_name):
    url3=requests.get("https://api.github.com/repos/{username}/{repo}/commits".format(username=user,repo=repo_name))
    json_object_3=url3.json()
    return render(request,'basic_app/commit_data.html',{"user_commit":json_object_3,"repo_name":repo_name})


@login_required
def contact_msg_store(request):
    enquiry=False
    if request.method=="POST":
        contact_message_1=ContactForm(data=request.POST)
        if contact_message_1.is_valid():
            contact_me_message=contact_message_1.save()
            contact_me_message.save()
            enquiry=True
    else:
        contact_message_1=ContactForm()
    return render(request,'basic_app/contact_me.html',{"contact_message_1":contact_message_1,"enquiry":enquiry})
