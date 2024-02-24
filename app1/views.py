from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')#from input field name
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        
        if(password1!=password2):
            return HttpResponse("ur password was not entered correctly")
        else:
            my_user = User.objects.create_user(uname,email, password1)
            my_user.save()
        # return HttpResponse("user has been created successfully")
            return redirect('login')
        # print(uname,email,password1,password2)
    return render(request,'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')#from input field name
        password = request.POST.get('password')#from input field name
        print(uname,password)
        user = authenticate(request,username=uname,password=password)#match this with signup
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("username or password incorrect!!!")
            
    return render(request,'login.html')


def LogOut(request):
    logout(request)
    return redirect('login')

