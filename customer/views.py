from datetime import date
import datetime
from random import randint
from django.shortcuts import get_object_or_404, render,redirect
from eKart import settings
from .models import Customer, Cart, Order, OrderItem
from seller.models import Seller,Products
from eKart_admin.models import Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import F
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
# Create your views here.


def customer_home(request):
    products=Products.objects.all()
    return render(request, 'customer/customer_home.html',{'products':products})


def store(request):
    allcategory=Category.objects.all()
    query=request.GET.get('query','all')
    if query=='all':
        storeProducts=Products.objects.all()
    else:
        storeProducts=Products.objects.filter(product_category=query) 

    paginator=Paginator(storeProducts,2)
    page=request.GET.get('page')
    try:
        products=paginator.page(page)
    except PageNotAnInteger:
        products=paginator.page(1)
    except EmptyPage:
        products=paginator.page(paginator.num_pages)

              
        
    return render(request, 'customer/store.html',{'storeProducts':products,'allcategory':allcategory})


def product_detail(request,id):
    msg=''
    product=Products.objects.get(id=id)
    if request.method=='POST':
        if 'customer' in request.session:
            customer = Customer.objects.get(id = request.session['customer'])
            cart=Cart(customer= customer,product=product,price=product.price)
            cart.save()
            return redirect('customer:cart')
        else:
            target_url=reverse('customer:customer_login')
            
            redirect_url= target_url+ '?pid-' +str(id)
            return redirect(redirect_url)

        
    try:

        cart_item = get_object_or_404(Cart, customer = customer,product = id)
        item_exist = True
        


    except Exception as e:
         
        item_exist = False    
            
            
    
    return render(request, 'customer/product_detail.html',{'product':product,'item_exist':item_exist})


def cart(request):
    
    if 'customer' in request.session:
        carts=Cart.objects.filter(customer=request.session['customer'])
        grand_total = 0   
    
        cart = Cart.objects.filter(customer = request.session['customer']).annotate(grand_total = F('quantity') * F('product__price') )
        enable_checkout=True
        for item in cart:
            if item.product.stock<=0:
                enable_checkout=False
            grand_total += item.grand_total
        print(grand_total)
    else:
        return redirect('customer:customer_login')    
    
    
   
    return render(request, 'customer/cart.html',{'carts':carts,'grand_total': grand_total,'enable_checkout':enable_checkout})


def place_order(request):
    return render(request, 'customer/place_order.html')


def order_complete(request):
    return render(request, 'customer/order_complete.html')


def dashboard(request):
    return render(request, 'customer/dashboard.html')


def seller_register(request):
    message = ''
    status = False
    if request.method == 'POST':  
        first_name = request.POST['fname'] 
        last_name = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        company_name = request.POST['cmp_name']
        city = request.POST['city']
        country = request.POST['country']
        account_no = request.POST['acc_no']
        bank_name = request.POST['bank_name']
        branch = request.POST['branch']
        ifsc = request.POST['ifsc']
        pic = request.FILES['pic']
        




        
       
        seller_exist = Seller.objects.filter(email = email).exists()

        if not seller_exist: 

            seller = Seller(first_name = first_name, last_name = last_name, company_name = company_name,    gender = gender, email = email, 
                            city = city, country = country, account_no = account_no, bank_name = bank_name,
                            branch_name = branch, ifsc = ifsc, pic = pic)
            seller.save()
            message = 'Registration Succesful'
            status = True

        
        else:
            message = 'Email Exists'
    return render(request, 'customer/seller_register.html', {'message': message})


def seller_login(request):
    msg=''
    if request.method=='POST':
      seller_id=request.POST.get('seller_id')
      password=request.POST.get('password')
      try:
        seller=Seller.objects.get(login_id=seller_id,password=password)
        request.session['seller']=seller.id
        return redirect('Seller:seller_home')
      except:
          msg='Invalid username or password'

               
    return render(request, 'customer/seller_login.html',{'msg': msg})


def customer_signup(request):
    message = ''
    if request.method == 'POST':  # when user submit the form
        # here fname is the name attribute given in form input
        # fetching values from form data and storing in variable
        first_name = request.POST['fname'] 
        last_name = request.POST['lastname']
        email = request.POST['email']
        gender = request.POST['gender']
        city = request.POST['city']
        country = request.POST['country']
        password = request.POST['password']

        
        # use exists() method to check whether the user with given email exists, it returns boolean
        customer_exist = Customer.objects.filter(email = email).exists()

        if not customer_exist: 

            customer = Customer(first_name = first_name, last_name = last_name, gender = gender, email = email, 
                            city = city, country = country, password = password)
            customer.save()
            message = 'Registration Succesful'

        
        else:
            message = 'Email Exists'
   

    return render(request, 'customer/customer_signup.html', {'message': message})


def customer_login(request):
    msg=''
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        try:
            customer=Customer.objects.get(email=email,password=password)
            request.session['customer']=customer.id
            return redirect('customer:customer_home')
        except:
            msg='invalid email or password'
    return render(request, 'customer/customer_login.html',{'msg':msg})


def forgot_password_customer(request):
    return render(request, 'customer/forgot_password_customer.html')


def forgot_password_seller(request):
    return render(request, 'customer/forgot_password_seller.html')

def remove_item(request,item_id):
    item=Cart.objects.get(id=item_id)
    item.delete()

    return redirect('customer:cart')

def logout_customer(request):
    if "customer" in request.session:
        del request.session['customer']
    return redirect('customer:customer_login')

def update_cart(request):
    product_id = request.POST['id']
    qty = request.POST['qty']
    print(qty)
    grand_total = 0
    cart = Cart.objects.get(product = product_id)
    cart.quantity = qty
    cart.save()

    cart = Cart.objects.filter(customer = request.session['customer']).annotate(sub_total = F('quantity') * F('product__price') )
    
    for item in cart:
        grand_total += item.sub_total
    print(grand_total)
    # item_price = cart.product.price
    return JsonResponse({'status': 'Quantity updated', 'grand_total': grand_total})

def seller_logout(request):
    if "seller" in request.session:
        del request.session['seller']
    
    return redirect('customer:seller_login')    

def order_product(request):
    cart=Cart.objects.filter(customer=request.session['customer']).annotate(sub_total=F('quantity')*F('product__price'))

    customer=request.session['customer']
    grand_total=0
    for item in cart:
        grand_total+=item.sub_total

    order_amount=grand_total
    order_currency='INR'
    order_receipt='order_rcptid_11'
    notes={'shipping address':'bommanahalli,banglore'}

    order_no='OD-Ekart-'+ str(randint(1111111111,9999999999))

    client=razorpay.Client(auth=(settings.RZP_KEY_ID,settings.RZP_KEY_SECRET))
    payment=client.order.create({
        'amount':order_amount * 100,
        'currency':order_currency,
        'receipt':order_receipt,
        'notes':notes

    })
    order = Order(customer_id =customer, order_id = payment['id'], total_amount = grand_total, order_no = order_no )
    order.save()
    print(payment)
    return JsonResponse({'payment': payment})
        
@csrf_exempt        
def update_payment(request):
    if request.method == 'GET':
        return redirect('customer:customer_home')

    order_id = request.POST['razorpay_order_id']
    payment_id = request.POST['razorpay_payment_id']
    signature = request.POST['razorpay_signature']
    client = razorpay.Client(auth = (settings.RZP_KEY_ID, settings.RZP_KEY_SECRET))
    params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }
    signature_valid = client.utility.verify_payment_signature(params_dict)
    if signature_valid:
    
        order_details = Order.objects.get(order_id = order_id)
        order_details.payment_status = True
        order_details.payment_id = payment_id
        order_details.signature_id = signature
        
        order_details.order_status = 'order placed on ' + str(date.today())
        cart = Cart.objects.filter(customer = order_details.customer)

        for item in cart:
            order_item = OrderItem(order_id = order_details.id, customer =  order_details.customer, product_id = item.product.id, quantity = item.quantity, price = item.product.price )
            order_item.save()
            selected_qty = item.quantity
            selected_product = Products.objects.get(id = item.product.id)
            selected_product.stock -= selected_qty
            selected_product.save()
            

   
        order_details.save()
        cart.delete()

        order_items=OrderItem.objects.filter(order_id=order_details.id)
        
            


        # customer_name = request.session['customer_name']
        # order_number =  order_details.order_no
        # current_year = datetime.now().year
        
        # subject = "Order Confirmation"
        # from_email = settings.EMAIL_HOST_USER

        # to_email = ['suvarna@cybersquare.org']

        
        
        # html_content = render_to_string('customer/invoice.html', {
        # 'customer_name': customer_name,
        # 'order_no': order_number,
        # 'order_date': order_details.created_at,
        # 'current_year': current_year,
       
        # 'grand_total': order_details.total_amount
        
        # })
            
        # msg = EmailMultiAlternatives(subject, html_content, from_email, to_email)
        # msg.attach_alternative(html_content, "text/html")

 
        # msg.send()
        context={
            'order_items':order_items,
            'order_details':order_details,
            }
        return render(request, 'customer/order_complete.html',context  )
