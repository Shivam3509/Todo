import imp
from itertools import product
from multiprocessing import context
from xml.dom.pulldom import ErrorHandler
from django.http import HttpResponse
from django.shortcuts import redirect, render
from requests import Response, delete
from .models import Product,Customer,Order,Notification
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
import json
# Create your views here.
@login_required
def Items(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        all =Product.objects.create(name=data['product_name'],type = data['product_categorie'],avaliable = data['available_quantity'], price = data['price'])
        context['all'] =all
        return redirect('productlist')
    return render(request, 'items.html',context)

@login_required
def Saler(request):
    context = {}
    if request.method == 'POST':
        data = request.POST
        merchant =Customer.objects.create(name=data['customer_name'],shopname = data['shop_name'],address = data['address'])
        context['mer'] = merchant
        return redirect('customerlist')
    return render(request, 'saler.html')

@login_required
def order_shipping(request):
    if not request.user.is_superuser:
        return HttpResponse('your are not superuser to perform this action')
    context = {}
    product=Product.objects.all()
    notify = Notification.objects.filter(to_user=request.user, read=False).count()
    context['notify'] = notify
    customer=Customer.objects.all()
    if request.method == 'POST':
        data = request.POST
        quantity = data['quantity']
        pro = Product.objects.get(id=data['product_name'])
        cus = Customer.objects.get(id=data['customer'])
        total = pro.price * int(quantity)
        gst = (total * 18/100) + total
        Order.objects.create(product=pro,customer=cus,quantity=quantity,total=total,gst=gst)
        context['total'] = total
        context['gst'] = gst
        super_user_list = [user.id for user in User.objects.filter(is_superuser=True)]
        bulk_notify = [Notification(from_user=request.user,to_user_id=superuser_ids, message=f'{request.user.username} add the new product, ') for superuser_ids in super_user_list]
        Notification.objects.bulk_create(bulk_notify)
    all =Order.objects.all().order_by('-id')
    paginator = Paginator(all,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['product'] = product
    context['customer'] = customer
    

    return render(request, 'order.html',context)

@login_required
def Edit(request,id):
    context = {}
    notify = Notification.objects.filter(to_user=request.user, read=False).count()
    context['notify'] = notify
    update = Order.objects.get(id=id)
    product=Product.objects.all()
    customer=Customer.objects.all()
    if request.method == 'POST':
        update.customer_id = request.POST['customer_name']
        update.product_id = request.POST['product_name']
        update.quantity = request.POST['quantity']
        pro = Product.objects.get(id=request.POST['product_name'])
        total = pro.price * int(request.POST['quantity'])
        gst = (total * 18/100) + total
        update.total = total
        update.gst = gst
        update.save()
        super_user_list = [user.id for user in User.objects.filter(is_superuser=True)]
        bulk_notify = [Notification(from_user=request.user,to_user_id=superuser_ids, message=f'{request.user.username} has set the {request.POST["quantity"]} quantity of the {pro.name}, ') for superuser_ids in super_user_list]
        Notification.objects.bulk_create(bulk_notify)
        return redirect('/order')
    context['update'] =update
    context['product'] = product
    context['customer'] = customer
    return render(request, 'update.html', context)

def Delete(request,id,action):
    if request.method == 'GET':
        re = None
        if action == "order":
            task = Order.objects.get(id=id)
            re = '/order'
        elif action=="customer":
            task=Customer.objects.get(id=id)
            re = '/customerlist'
        elif action=="product":
            task=Product.objects.get(id=id)
            re='/productlist'
        task.delete()
        return redirect(re)

def Login(request):
    if request.method == 'POST':
        data=request.POST
        username = data['username']
        password = data['password']
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('customerlist')
        messages.error(request,'Invalid Credentials')
        return redirect('login')
    return render(request,'login.html')

def Logout(request):
    logout(request)
    return redirect('login')

def AddUser(request):
    user = User.objects.all()
    if not request.user.is_superuser:
        return HttpResponse('your are not superuser to perform this action')

    if request.method == 'POST':
        data= request.POST
        
        password = make_password(data['password'])
        if User.objects.filter(email__exact=data['email']).first():
            messages.success(request, 'This email is already taken')
            return redirect('add')

        if User.objects.filter(username__exact=data['username']).first():
            messages.success(request, 'This username is already taken')
            return redirect('add')

        if data['confirm_password'] != data['password']:
            messages.success(request, 'Your password does not match')
            return redirect('add')

       
        staff=data.get('staff',None)


        if staff and staff == '1':
            add = User.objects.create(username=data['username'],email=data['email'],password=password, is_staff=True)
        elif staff and staff == '2':
            add = User.objects.create(username=data['username'],email=data['email'],password=password, is_superuser=True)
        elif staff and staff == '3':
            add = User.objects.create(username=data['username'],email=data['email'],password=password, is_staff=True , is_superuser=True)
        else:
            add = User.objects.create(username=data['username'],email=data['email'],password=password)
        return redirect('login')
    return render(request,'addusers.html')

def UpdateProduct(request,id):
    context = {}
    update = Product.objects.get(id=id)
    if request.method == 'POST':
        data =request.POST
        update.name = data['product_name']
        update.type = data['product_type']
        update.avaliable = data['product_avalibilty']
        update.price = data['product_price']
        update.save()
        return redirect('productlist')
    context['update'] = update
    return render(request,'updateproduct.html', context)

def UpdateCustomer(request,id):
    context = {}
    update = Customer.objects.get(id=id)
    if request.method == 'POST':
        data =request.POST
        update.name = data['customer_name']
        update.shopname = data['shop_name']
        update.address = data['customer_address']
        update.save()
        return redirect('customerlist')
    context['update'] = update
    return render(request,'updatecustomer.html',context)

def UserList(request):
    context = {}
    alluser = User.objects.all()
    context['alluser'] = alluser
    return render(request,'userlist.html',context)

def notify(request):
    context = {}
    notification = Notification.objects.filter(to_user=request.user).order_by('-id')
    context['read_noti'] = notification.filter(read=True)
    context['unread_noti'] = notification.filter(read=False)
    if request.method == "POST":
        notification.update(read=True)
        return HttpResponse({})
    return render(request, 'notification.html', context)

def side(request):
    return render(request,'sidebar.html')

def Product_List(request):
    context = {}
    all = Product.objects.all().order_by('-id')
    context['all'] = all
    return render(request, 'productlist.html', context)

def Customer_List(request):
    context = {}
    all = Customer.objects.all().order_by('-id')
    context['all'] = all
    return render(request, 'customerlist.html', context)

def price_product(request):
    context={}
    if request.method=="POST":
        product_id = request.POST['product']
        abc = Product.objects.get(id=product_id)
        context['price'] = abc.price
        context['avaliable_quantity'] = abc.avaliable
        return HttpResponse(json.dumps(context))


