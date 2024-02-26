from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.html import strip_tags
import random
import string
# Create your views here.



# @login_required(login_url='login')
# def HomePage(request):
#     if request.method == 'POST':
#         uname = request.POST.get('username')  # from input field name
#         email = request.POST.get('email')
#         message = request.POST.get('message')
        
#         # List of email addresses to which the message will be sent
#         recipient_emails = ['fidha@cybersquare.org', email]  # Adding email from the form
        
#         # Send email to each recipient in the list
#     #     for recipient_email in recipient_emails:
#     #         send_mail(
#     #             'contact',  # subject
#     #             message,  # message
#     #             settings.EMAIL_HOST_USER,  # from email address
#     #             [recipient_email],  # to email address
#     #             fail_silently=False
#     #         )
#     # return render(request, 'home.html')

       
@login_required(login_url='login')
def HomePage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')  # from input field name
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # List of email addresses to which the message will be sent
        recipient_emails = ['fidha@cybersquare.org', email]  # Adding email from the form
        random_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
        
        # Render the HTML template
        context = {'username': uname, 'email': email, 'message': message, 'random_string': random_string}
        html_content = render_to_string('email_template.html', context)
        
        # Create an EmailMultiAlternatives object
        msg = EmailMultiAlternatives(
            subject='Email Verification',
            body=strip_tags(html_content),  # Plain text version of the email
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_emails,
        )
        
        # Attach the HTML content to the email
        msg.attach_alternative(html_content, "text/html")
        
        # Send the email
        msg.send()
    return render(request, 'home.html')    
    


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

