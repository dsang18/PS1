from django.shortcuts import render, HttpResponse, redirect
from .models import *
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
import json
from django.conf import settings



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

    if request.method=="POST":
        fullname = request.POST.get("fullname","")
        phone = request.POST.get("phone","")
        password1 = request.POST.get("password","")
    
        new_user = Farmer(fullname=fullname, password=password1, phone=phone)
        new_user.save()
        return redirect('/farmer-login')
    return render(request, 'farmer_register.html')

def customer_register(request):

    # user_details = Customer.objects.filter(id=id)
    all_numbers = list(Customer.objects.values_list("phone",flat=True))
    # print(all_numbers)

    if request.method=="POST":
        fullname = request.POST.get("fullname","")
        phone = request.POST.get("phone","")
        password1 = request.POST.get("password","")
        email = request.POST.get("email","")
        address = request.POST.get("address","")

        new_user = Customer(fullname=fullname, password=password1, phone=phone, email=email, address=address)
        new_user.save()
        return redirect("/customer-login/")
    return render(request, 'customer_register.html',{"all_numbers":all_numbers})

def home(request, user_type, id):
    update = 0
    user_details = Customer.objects.filter(id=id)
    all_produce = FoodGrains.objects.all()
    if user_type=='farmer':
        update=1
        user_details = Farmer.objects.filter(id=id)
        all_produce = FoodGrains.objects.filter(farmer=user_details[0])
    return render(request, 'home.html', {'update':update, "user":user_details[0], "all_produces":all_produce})

def profile(request):
    return render(request, 'profile.html')

def add_product(request, user_type, id):
    farmer = Farmer.objects.filter(id=id)
    if request.method=="POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        image = request.POST.get("image")

        new_produce = FoodGrains(farmer=farmer[0], name=name, price=price, quantity=quantity, image=image)
        new_produce.save()
        return redirect(f"/{user_type}/{id}/home/")

    return render(request, 'add_product.html', {'user_type':user_type, 'id':id})

def update_product(request, user_type, id, prod_id):
    produce = FoodGrains.objects.filter(id=prod_id)
    if request.method=="POST":
        if "update" in request.POST:
            name = request.POST.get("name")
            price = request.POST.get("price")
            quantity = request.POST.get("quantity")
            image = request.POST.get("image")
            produce = FoodGrains.objects.get(id=prod_id)
            produce.name = name
            produce.price = price
            produce.quantity = quantity
            if image:
                produce.image = image
            produce.save()
        elif "delete" in request.POST:
            FoodGrains.objects.filter(id=prod_id).delete()
        return redirect(f'/{user_type}/{id}/home/')
    return render(request, 'update_product.html',{'user_type':user_type, 'id':id, 'produce':produce[0]})

