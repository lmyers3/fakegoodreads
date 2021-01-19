from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User

# Create your views here.

def index(request):
    return render(request, "login/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "home/search.html")
        else:
            return HttpResponse("could not log you in")
    else:
        return render(request, "login/index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return HttpResponse("error passwords do not match")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, None, password)
            user.save()
        except IntegrityError:
            return HttpResponse("error username has already been created")
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login/register.html")
