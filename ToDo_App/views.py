from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from datetime import date
from .models import Tasks_List
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    # Checks if the user is authenticated, if yes redirects them to ToDo Main Page.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('ToDo_App:ToDo'))

    # index.html is the landing page of the WebApp if user is not authenticated.
    
    return render(request, "ToDo_App/index.html")


def signup(request):
    # Takes care of the SignUp Process, after the new user has entered his detail.
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)

        # Collecting of basic info regarding a new user.
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            # Checking if the username is unique.
            if User.objects.filter(username__iexact=username).exists():
                message = "Username is already in use."
                return render(request, "ToDo_App/signup.html", {"form": forms.SignupForm(), "message": message})

            # Checking if the email is unique
            if User.objects.filter(email__iexact=email).exists():
                message = "Email already in use"
                return render(request, "ToDo_App/Tsignup.html",
                              {"form": forms.SignupForm(), "message": message})

            # If the username,email are unique and passwords match the user object is created and saved to the User Table in the database
            user = User.objects.create_user(username, email, form.cleaned_data.get('password'))
            user.save()

            # User is logged in here and is redirected to the main page
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("ToDo_App:ToDo"))

            return HttpResponseRedirect(reverse("ToDo_App:ToDo"))


    else:
        return render(request, "ToDo_App/signup.html", {"form": forms.SignupForm()})


def login_page(request):
    # Takes in login info using a form and then authenticates it.
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        # Check's if the user is present in the User DB, if present the user is Re-directed to ToDo Main Page
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("ToDo_App:ToDo"))

        # If the user is not present in the User Model, Invalid credentials message shows up.
        else:
            return render(request, "ToDo_App/login.html", {"message": "Invalid Credentials!"})

    return render(request, "ToDo_App/login.html")


def logout_view(request):
    # Logs out the user
    logout(request)
    return render(request, "ToDo_App/logout.html")

@login_required
def ToDo(request):
    # Welcome to the main page of the WebApp.
    today = date.today()

    # user variable is set in the name of currently logged in user.
    user = request.user

    # tasks variable is set to all records in the Tasks_List table associated with the currently logged in user.
    tasks = user.tasks_list_set.all()

    # code if the request.method is POST
    if request.method == "POST":
        # task_to_be_added variable stores the task to be added that is sent via the post request.
        task_to_be_added = request.POST["tasks"]

        # Checks if the task_to_be_added is empty.
        if task_to_be_added:
            new_task = user.tasks_list_set.create(task=task_to_be_added, logged_user=user)
            return render(request, "ToDo_App/ToDo.html", {"tasks": tasks, "today_date": today})

        # else is used to display a message in case of a empty task_to_be_added.
        else:
            message = "Empty task!! C'mon you can be MORE PRODUCTIVE."
            return render(request, "ToDo_App/ToDo.html", {"tasks": tasks, "today_date": today, "message": message})

    tasks = user.tasks_list_set.all()
    return render(request, "ToDo_App/ToDo.html", {"tasks": tasks})


def Update_Task(request, pk):
    # user variable is set to cirrenty logged in user .
    user = request.user

    # Task variable is given value of the TASK that needed to be updated.
    task = Tasks_List.objects.get(id=pk)

    # Form with an instance of the task that needs to be updated.
    form = forms.TaskForm(instance=task)

    # Code for request method  POST
    if request.method == 'POST':

        # The form is used to update the task.
        form = forms.TaskForm(request.POST, instance=task)
        if form.is_valid():
            # the updated task is then stored to the Task_list table in Database.
            form.save()
            tasks = user.tasks_list_set.all()
            return HttpResponseRedirect(reverse("ToDo_App:ToDo"), {"tasks": tasks})

    context = {"form": form}
    return render(request, "ToDo_App/update_task.html", context)


def Delete_Task(request, pk):
    user = request.user
    task = Tasks_List.objects.get(id=pk)

    # Deleting the task.
    task.delete()

    tasks = user.tasks_list_set.all()
    return HttpResponseRedirect(reverse("ToDo_App:ToDo"), {"tasks": tasks})

