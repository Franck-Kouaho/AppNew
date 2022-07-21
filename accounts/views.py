from cmath import exp
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from accounts.models import CustomUser

# Create your views here.
User = get_user_model()

def signup(request):
    if request.method == 'POST':
        #traiter le formulaire
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confpassword = request.POST.get("conf_password")
        if password == confpassword:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            login(request=request, user=user)
            return JsonResponse(data={
                "username" : username,
                "is_connect" : user.is_authenticated,
                "message" : "Utilisateur connecté"
            })
    if request.user.is_authenticated :
        message = "Utlisateur déja connecté !"
        username = request.user.username
    else:
        message = "Utlisateur non connecté verifier les données de conection !"
        username = ""
    return JsonResponse(data={
        "is_connect" : request.user.is_authenticated,
        "message" : message,
        "username" : username
    })

def login_user(request):
    if request.method == 'POST':
        #traiter le formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
            else:
                users = CustomUser.objects.filter(email=username)
                user = authenticate(username=users[0].username, password=password)
                login(request, user)
            if(user.is_authenticated):
                return JsonResponse(data={
                    "is_connect" : request.user.is_authenticated,
                    "username" : user.get_username()
                })
        except:
            pass
    if request.user.is_authenticated :
        message = "Utlisateur déja connecté !"
        username = request.user.username
    else:
        message = "Utlisateur non connecté verifier les données de conection !"
        username = ""
    return JsonResponse(data={
        "is_connect" : request.user.is_authenticated,
        "message" : message,
        "username" : username
    })

def logout_user(request):
    logout(request=request)
    return JsonResponse(data={
        "is_connect" : request.user.is_authenticated,
        "username" : ""
    }) 

def myProfile(request):
    if not request.user.is_authenticated:
        return redirect('accueil')
    context = {
        "user" : request.user
    }
    template = loader.get_template("accounts/index.html")
    return HttpResponse(template.render(context, request))