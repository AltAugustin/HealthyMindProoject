from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Questionairre
from django.http import HttpResponse
from deployment_ready import main_function

# Create your views here.
def continueasguest(request):
    request.session['username'] = "guest"
    return render(request, "home.html")
def index(request):
    if "username" not in request.session:
        if request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user =  authenticate(username = username, password=password) 
            if not user:
                return render(request, "index.html", {"nouserexists": True})
            else:
                request.session['username'] = username
                return render(request, "home.html")
        return render(request, "index.html")
    else:
        return render(request, "home.html")


def signup(request):
    return render(request, "signup.html")

def logout(request):
    if "username" in request.session:
        del request.session['username']
    return render(request, "index.html")

def home(request):
    if "username" not in request.session:
        return render(request, "index.html")

    return render(request, "home.html")

def results(request):
    if "username" not in request.session:
        return render(request, "index.html")

    imageFile = open("textfile.txt","r+") 
    txt = imageFile.read()
    # txt = txt.decode('UTF-8')
    img_str = main_function(txt)
    # lists = img_str.strip('][').split(', ')
    return render(request, "results.html", {"imgstr": img_str, "datacoming": True, "a": img_str[0], "b": img_str[1], "c": img_str[2]})

def test(request):
    if "username" not in request.session:
        return render(request, "index.html")
    if request.POST:
        answer1 = request.POST.get("answer1")
        answer2 = request.POST.get("answer2")
        answer3 = request.POST.get("answer3")
        answer4 = request.POST.get("answer4")
        answer5 = request.POST.get("answer5")
        answer6 = request.POST.get("answer6")
        username = request.session['username']
        questions = Questionairre.objects.create(username=username,
                                    answerone = answer1,
                                    answertwo = answer2,
                                    answerthree = answer3,
                                    answerfour = answer4,
                                    answerfive = answer5,
                                    answersix = answer6)
        file1 = open("textfile.txt","w")
        
        # \n is placed to indicate EOL (End of Line)
        file1.write(answer1+"\n")
        file1.write(answer2+"\n")
        file1.write(answer3+"\n")
        file1.write(answer4+"\n")
        file1.write(answer5+"\n")
        file1.write(answer6+"\n")
        file1.close() #to change file access modes
        imageFile = open("textfile.txt","r+") 
        txt = imageFile.read()
        # txt = txt.decode('UTF-8')
        img_str = main_function(txt)
        # lists = img_str.strip('][').split(', ')
        return render(request, "results.html", {"imgstr": img_str, "datacoming": True, "a": img_str[0], "b": img_str[1], "c": img_str[2]})

    return render(request, "test.html")

def createnewuser(request):
    from django.contrib.auth.models import User
    username = request.POST.get("username")
    usernamecount = User.objects.filter(username = username).count()
    if usernamecount>0:
         return render(request, "signup.html", {"usernameexists": True})
    email = request.POST.get("email")
    emailcount = User.objects.filter(email = email).count()
    if emailcount>0:
         return render(request, "signup.html", {"emailexists": True})
    password = request.POST.get("password")
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password)
    return render(request, "index.html", {"usercreated": True})
