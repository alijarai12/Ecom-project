from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import decimal
from shop_project import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str

from . tokens import generate_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.
def index(request):
    product = Product.objects.all()

    return render(request, 'app/index.html', {'product':product})

def productdetail(request, pk):
    product = Product.objects.filter(id=pk)
    return render(request, 'app/productdetail.html', {'product':product})

def register(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
      
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username")
            return redirect('register')

        # if User.objects.filter(email=email):
        #     messages.error(request, "Email already registered")

        if len(username)>10:
            messages.error(request, "Username must be 10 character")

        if pass1!=pass2:
            messages.error(request, "Password didn't match!")
            return redirect('register')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name= fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()
        messages.success(request, "your account has been successfully created. we have send u a email, please confirm your email in order to activate your account ")
    
    #Welcome Email
        subject = "welcome to our website - E-Shopping"
        message = "Hello  " + myuser.first_name + "!!\n" + "Welcome to LS!! \n  Thank u for visiting our website \n We have also send you a confirmation email, please confirm youe email address in order to activate"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

 #Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ - E-Shopping!!"
        message2 = render_to_string('email_confirmation.html',{
            'name' : myuser.first_name,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token' : generate_token.make_token(myuser)
            })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('register')
    return render(request, "account/register.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('index')
    else:
        return render(request, 'activation_failed.html')

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=product_id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()
    
    return redirect('cart')

@login_required
def cart(request):
    user = request.user
    cart_products = Cart.objects.filter(user=user)

    amount = decimal.Decimal(0)
    cp = [p for p in Cart.objects.all() if p.user==user]
    if cp:
        for p in cp:
            temp_amount = (p.quantity * p.product.price)
            amount += temp_amount
    context = {
        'cart_products': cart_products,
        'amount': amount,
        'total_amount': amount ,
       }

    return render(request, 'app/cart.html', context)

@login_required
def remove_cart(request, cart_id):
    if request.method == 'GET':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        
    return redirect('cart')

@login_required
def plus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('cart')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'GET':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('cart')

@login_required
def checkout(request):
    user = request.user
    address_id = request.GET.get('address')
    payment = request.GET.get('payment')

    # Get all the products of User in Cart
    cart = Cart.objects.filter(user=user)
    for c in cart:
        # Saving all the products from Cart to Order
        Order(user=user, address=address_id, product=c.product, quantity=c.quantity,payment_method=payment).save()
        # And Deleting from Cart
        c.delete()
    return redirect('cart')

@login_required
def orders(request):
    all_orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    return render(request, 'app/orders.html', {'orders': all_orders})

def caty(request):
    categories = Category.objects.all()

    context = {
        "categories": categories,
    }
    return render(request,'app/cat.html', context)

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'account/profile.html', {'orders':orders})

