from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.urls import reverse
from database.email import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from database.models import Contact
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'index.html')
def network(request):
    return render(request,'network+.html')
def soccourse(request):
    return render(request,'SOCCourse.html')
def devops(request):
    return render(request,'DevOps.html')
def checkpoint(request):
    return render(request,'Checkpoint.html')
def ceh(request):
    return render(request,'CertifiedEthicalHacker.html')
def PCNSA(request):
    return render(request,'PaloAltoNetworks.html')
def CCNA(request):
    return render(request,'CCNA.html')
def mars(request):
    return render(request,'mars.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        course = request.POST.get('Course')
        msg = request.POST.get('message')

        contact = Contact(
            name = name,
            phone = phone,
            email = email,
            course =  course,
            msg = msg,


        )
        contact.save()
        messages.success(request , 'Message is Sent')
        return redirect('home')

    return redirect('home')

def dashboardlogin(request):
    if request.method == "POST":
        user = EmailBackend.authenticate(request,
                                        username=request.POST.get('username'),
                                        password=request.POST.get('password'),)
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                return redirect(reverse('dashboard'))
            elif user_type == '2':
                return HttpResponse("not found")
            elif user_type == '3':
                return HttpResponse('notfound')
            else:
                messages.error(request,'Email and Password Are Invalid !')
                return redirect('login')
        else:
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('login')
    return render(request,'dashboard\\pages-login.html')

def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")
@login_required(login_url='/login/')
def dashboardindex(request):
    contact = Contact.objects.all().order_by('-id')[:10] 
    data = {'contact':contact}
    return render(request,'dashboard\\index.html',data)

