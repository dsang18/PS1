from django.shortcuts import render, HttpResponse, redirect
from .models import *
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
import json
from django.conf import settings
from django.core.files.storage import FileSystemStorage


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
    if "add_to_cart" in request.POST:
        produce_item = request.POST.get("produce_item")
        get_produce = FoodGrains.objects.filter(id=produce_item)
        all_items_in_cart = cart.objects.filter(customer=user_details[0])
        all_items_list = []
        for i in all_items_in_cart:
            all_items_list.append(i.FoodGrains.name)

        if get_produce[0].name in all_items_list:
            pass
        else:
            new_item_in_cart = cart(customer=user_details[0],FoodGrains=get_produce[0],quantity=1)
            new_item_in_cart.save()
    return render(request, 'home.html', {'update':update, "user":user_details[0], "all_produces":all_produce})

def profile(request):
    return render(request, 'profile.html')

def add_product(request, user_type, id):
    farmer = Farmer.objects.filter(id=id)
    if request.method=="POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        # image = request.POST.get("image")
        request_file = request.FILES['image'] if 'image' in request.FILES else None
        if request_file:
            # save attached file
            print("X")
            # create a new instance of FileSystemStorage
            fs = FileSystemStorage()
            file = fs.save(request_file.name, request_file)
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
            fileurl = fs.url(file)
        
            new_produce = FoodGrains(farmer=farmer[0], name=name, price=price, quantity=quantity, image=fileurl)
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
            # image = request.POST.get("image")
            produce = FoodGrains.objects.get(id=prod_id)
            request_file = request.FILES['image'] if 'image' in request.FILES else None
            if request_file:
            # save attached file
            # create a new instance of FileSystemStorage
                fs = FileSystemStorage()
                file = fs.save(request_file.name, request_file)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = fs.url(file)
                produce.image = fileurl

            produce.name = name
            produce.price = price
            produce.quantity = quantity
            produce.save()
        elif "delete" in request.POST:
            FoodGrains.objects.filter(id=prod_id).delete()
        return redirect(f'/{user_type}/{id}/home/')
    return render(request, 'update_product.html',{'user_type':user_type, 'id':id, 'produce':produce[0]})

def view_cart(request, user_type, id):
    user_details = Customer.objects.filter(id=id)
    all_items_in_cart = cart.objects.filter(customer=user_details[0]).values('FoodGrains')
    all_items_qty_in_cart = cart.objects.filter(customer=user_details[0]).values('quantity')
    all_ids = []
    for i in all_items_in_cart:
        all_ids.append(i['FoodGrains'])
    all_prods = FoodGrains.objects.filter(id__in=all_ids)

    if "remove" in request.POST:
        prod_id = request.POST.get("prod_id")
        produce_query = FoodGrains.objects.get(id=prod_id)
        cart.objects.filter(customer=user_details[0], FoodGrains=produce_query).delete()
        return redirect(f'/{user_type}/{id}/home/cart/')
    return render(request, 'cart.html',{"items_in_cart":all_prods, "qtys":all_items_qty_in_cart,"user_type":user_type, "id":id})