from django.shortcuts import render
from eKart_admin.models import Category
from .models import Products


# Create your views here.
def seller_home(request):
    return render(request, 'seller/seller_home.html')

def add_product(request):
    msg=''
    addCategory=Category.objects.all()
    if request.method=='POST':
        product_category=request.POST.get('product_category')
        product_name=request.POST['product_name']
        product_no=request.POST['product_no']
        description=request.POST['description']
        stock=request.POST['stock']
        price=request.POST['price']
        image=request.FILES['image']
        
        productexist=Products.objects.filter(product_no= product_no).exists()
        if not productexist:
            product=Products.objects.create(
                product_category=product_category,
                product_name=product_name,
                product_no=product_no,
                description=description,
                stock=stock,
                price=price,
                image=image,
                seller_id=request.session['seller']

            )
            msg='product added'
        else:
            msg='product already exist'

    return render(request, 'seller/add_product.html',{'addCategory':addCategory, 'msg':msg})



def add_category(request):
    return render(request, 'seller/add_category.html')

def view_category(request):
    return render(request, 'seller/view_category.html')

def view_products(request):
    products=Products.objects.filter(seller_id=request.session['seller'])
    return render(request, 'seller/view_product.html',{'products':products})

def profile(request):
    return render(request,'seller/profile.html')

def view_orders(request):
    return render(request,'seller/view_orders.html')

def update_stock(request):
    return render(request,'seller/update_stock.html')

def order_history(request):
    return render(request,'seller/order_history.html')

