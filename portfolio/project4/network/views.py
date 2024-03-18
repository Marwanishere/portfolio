from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core import serializers

from .models import User
from .models import Tweet
from .models import FS



def index(request):
    pageNumber = int(request.GET.get('page', 1))
    nextPageUrl = '?page=' + str(pageNumber + 1)
    lastPageUrl = '?page=' + str(pageNumber - 1) if pageNumber > 1 else ""
    displacementAmount = (pageNumber - 1) * 10
    old_posts = Tweet.objects.all().order_by("-timestamp")[displacementAmount:displacementAmount+10]
    morePosts = Tweet.objects.all().order_by("-timestamp")[displacementAmount+10:displacementAmount+20].exists()
    return render(request, "network/index.html", {'old_posts': old_posts, 'nextPageUrl': nextPageUrl , 'lastPageUrl': lastPageUrl, "more_posts":morePosts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def npost(request):
    if request.method != "GET":
        dataPool = json.loads(request.body)
        new_post = Tweet.objects.create(
            user=request.user,
            content=dataPool['content'],
            title=dataPool["title"]
        )
        return JsonResponse({'message': 'Post generated successfully.'}, status=201)
    # above line acquired through cs50 chatbot prompting
    return HttpResponseRedirect(reverse("index"))

def delete_post(request, post_id):
    post_id = json.loads(request.body)['id']
    user = request.user
    old_posts = Tweet.objects.get(id = post_id)
    if user == old_posts.user or user.is_superuser:
        old_posts.delete()
    remaining_posts = Tweet.objects.all()
    return render(request, "network/index.html", {'remaining_posts': remaining_posts})

def smprofile(request, username):
    pageNumber = int(request.GET.get('page', 1))
    nextPageUrl = '?page=' + str(pageNumber + 1)
    lastPageUrl = '?page=' + str(pageNumber - 1) if pageNumber > 1 else ""
    displacementAmount = (pageNumber - 1) * 10
    # request.user gives you the user who made the request, please memorise this.
    user_logged_in = request.user
    user2unfollow = User.objects.get(username=username)
    # the get_or_create will return a tuple which will contain the object and a boolean indicating whether the thing was created 
    followstatus, created = FS.objects.get_or_create(follower=user_logged_in, following=user2unfollow)
    followstatus.delete()
    selected_users_old_posts = Tweet.objects.filter(user__username=username).order_by("-timestamp")[displacementAmount:displacementAmount+10]
    morePosts = Tweet.objects.filter(user__username=username).order_by("-timestamp")[displacementAmount+10:displacementAmount+20].exists()
    return render(request, "network/smprofile.html", {"selected_users_old_posts": selected_users_old_posts, "username": username, 'nextPageUrl': nextPageUrl , 'lastPageUrl': lastPageUrl, "more_posts":morePosts})

def smprofilefollowing(request, username): 
    pageNumber = int(request.GET.get('page', 1))
    nextPageUrl = '?page=' + str(pageNumber + 1)
    lastPageUrl = '?page=' + str(pageNumber - 1) if pageNumber > 1 else ""
    displacementAmount = (pageNumber - 1) * 10
    user_logged_in = request.user
    user2unfollow = User.objects.get(username=username)
    followstatus, created = FS.objects.get_or_create(follower=user_logged_in, following=user2unfollow)
    selected_users_old_posts = Tweet.objects.filter(user__username=username).order_by("-timestamp")[displacementAmount:displacementAmount+10]
    morePosts = Tweet.objects.filter(user__username=username).order_by("-timestamp")[displacementAmount+10:displacementAmount+20].exists()
    return render(request, "network/smprofilefollowing.html", {"selected_users_old_posts": selected_users_old_posts, "username": username, 'nextPageUrl': nextPageUrl , 'lastPageUrl': lastPageUrl, "more_posts":morePosts})
    
def followingpage(request):
    pageNumber = int(request.GET.get('page', 1))
    nextPageUrl = '?page=' + str(pageNumber + 1)
    lastPageUrl = '?page=' + str(pageNumber - 1) if pageNumber > 1 else ""
    displacementAmount = (pageNumber - 1) * 10
    users_followed = FS.objects.filter(follower = request.user).values_list('following', flat = True)
    old_posts = Tweet.objects.filter(user__in=users_followed).order_by("-likes" , "-timestamp")[displacementAmount:displacementAmount+10]
    morePosts = Tweet.objects.filter(user__in=users_followed).order_by("-likes" , "-timestamp")[displacementAmount+10:displacementAmount+20].exists()
    return render(request, "network/followingpage.html", {'old_posts': old_posts, 'nextPageUrl': nextPageUrl , 'lastPageUrl': lastPageUrl, "more_posts":morePosts})

def edit_post(request, id):
    # skeleton of below function made with the assistance of the course's ai chatbot
    if request.method == "POST":
        #below line format made using cs50.ai assistance
        contentpool = json.loads(request.body)
        p0st = Tweet.objects.get(id = id)
        #below line format made using cs50.ai assistance
        p0st.content=contentpool['content']
        p0st.save()

def liked_post(request, id):
    if request.method == "POST":
        alllikes = json.loads(request.body)
        liked1 = Tweet.objects.get(id = id)
        liked1.liked = alllikes['liked']
        liked1.save()
        return JsonResponse({'success': liked1})


    

