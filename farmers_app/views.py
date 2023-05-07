from django.shortcuts import render, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

def choice(request):
    return render(request, 'choice.html')

def customer_login(request):
    if request.method=="POST":
        phone_no = request.POST.get("phone")
        password = request.POST.get("password")
        try:
            user_details = Customer.objects.filter(phone=phone_no)
            hash_pwd = user_details[0].password
            print(user_details)
            if check_password(password, hash_pwd):
                
                return HttpResponse(f"/customer/{str(user_details[0].id)}/home/")
            else:
                return HttpResponse("Password Mismatch")

        
        except Exception as e:
            print(e)
            if not user_details:
                return HttpResponse("No user with above credentials")
            elif password!=user_details[0].password:
                return HttpResponse("Incorrect password for above user")
            else:
                return HttpResponse("Invalid credentials")
    return render(request, 'customer_login.html')

def farmer_login(request):
    if request.method=="POST":
        phone_no = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user_details = Farmer.objects.filter(phone=phone_no)
            hash_pwd = user_details[0].password
            
            if check_password(password, hash_pwd):
                return HttpResponse(f"/farmer/{str(user_details[0].id)}/home/")
            else:

                return HttpResponse("Password Mismatch")

        
        except Exception as e:
            print(e)
            if not user_details:
                return HttpResponse("No user with above credentials")
            elif password!=user_details[0].password:
                return HttpResponse("Incorrect password for above user")
            else:
                return HttpResponse("Invalid credentials")
            
    return render(request, 'farmer_login.html')

def farmer_register(request):
    all_numbers = list(Farmer.objects.values_list("phone",flat=True))
    # print(all_numbers)

    if request.method=="POST":
        fullname = request.POST.get("fullname","")
        phone = request.POST.get("phone","")
        password1 = request.POST.get("password","")
    
        new_user = Farmer(fullname=fullname, password=password1, phone=phone)
        new_user.save()
    return render(request, 'farmer_register.html')

def customer_register(request):

    # user_details = Customer.objects.filter(id=id)
    all_numbers = list(Customer.objects.values_list("phone",flat=True))
    print(all_numbers)

    if request.method=="POST":
        fullname = request.POST.get("fullname","")
        phone = request.POST.get("phone","")
        password1 = request.POST.get("password","")
        email = request.POST.get("email","")
        address = request.POST.get("address","")

        new_user = Customer(fullname=fullname, password=password1, phone=phone, email=email, address=address)
        new_user.save()
    return render(request, 'customer_register.html',{"all_numbers":all_numbers})

def home(request, user_type, id):
    update = 0
    if user_type=='farmer':
        update=1

    return render(request, 'home.html', {'update':update})

def profile(request):
    return render(request, 'profile.html')

def add_product(request, user_type, id):
    return render(request, 'add_product.html')

def update_product(request):
    return render(request, 'update_product.html')

