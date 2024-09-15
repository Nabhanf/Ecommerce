from random import randint
from django.shortcuts import render,redirect
from .models import Admin_login, Category
from seller.models import Seller
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
def admin_home(request):
    return render(request,'ekart_admin/admin_home.html')

def view_category(request):
    categories=Category.objects.all()
    return render(request,'ekart_admin/view_category.html',{'categories': categories})

def add_category(request):
    msg=''
    if request.method=='POST':
        categoryname=request.POST['category_name']
        description=request.POST['description']
        image=request.FILES['image']
        
        categoryexist=Category.objects.filter(categoryname= categoryname).exists()
        if not categoryexist:
            category=Category.objects.create(
                categoryname=categoryname,
                description=description,
                image=image
            )
            msg='category added'
        else:
            msg='category already exist'    
            
    return render(request,'ekart_admin/add_category.html',{'msg': msg})

def pending_sellers(request):
    pending=Seller.objects.filter(status='pending')

    return render(request,'ekart_admin/pending_sellers.html',{'list':pending})

def approved_sellers(request):
    return render(request,'ekart_admin/approved_sellers.html')

def customers(request):
    return render(request,'ekart_admin/customers.html')

def admin_login(request):
    msg=''
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        try:
            admin=Admin_login.objects.get(username= username, password= password)
            request.session['admin']=admin.id
            return redirect('ekart_admin:admin_home')
        except:
            msg='invalid username or password'    
    return render(request,'ekart_admin/admin_login.html',{'msg': msg})

def approve_seller(request,id):

    seller = Seller.objects.get(id = id)
    seller_id = randint(11111, 999999)
    temporary_password = 'sel-' + str(seller_id)  
    subject = 'username and temporary password'
    message = 'Hi! your Ekart account has been approved, your seller id is ' + str(seller_id)  + ' and temporary password is ' + str(temporary_password)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [seller.email,]

    send_mail(
        subject = subject,
        message = message,
        from_email = from_email,
        recipient_list = recipient_list
    )

    Seller.objects.filter(id = id).update(login_id = seller_id, password = temporary_password, status = 'active')

    return redirect('ekart_admin:pending_sellers')

def admin_logout(request):
    if "admin" in request.session:
        del request.session['admin']
    return redirect('ekart_admin:admin_login')
