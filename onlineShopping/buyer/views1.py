from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from buyer.models import Customer, Cart, Products, Brands, OrderProduct, Orders
from buyer.forms import UpdateProfileForm, CheckoutForm

def home(request):
    return render(request, 'home1.html')

def products(request):
    current_user = request.user
    
    brands = Brands.objects.all()

    brandid = request.GET.get('brand', None)
    filtered_brand = None

    if brandid:
        products = Products.objects.filter(brand_id=brandid)
        filtered_brand = Brands.objects.get(id=brandid)
    else:
        products = Products.objects.all()
    
    n = len(products)

    carts = Cart.objects.filter(user_id=current_user.id)
    qty = sum(cart.qty for cart in carts)
    total = sum(cart.amount for cart in carts)

    params = {
        'products': products,
        'brands': brands,
        'filtered_brand': filtered_brand,
        'n': n,
        'qty': qty,
        'total': total,
        'carts': carts,
    }
    
    return render(request, 'Buyer/products.html', params)




def searchMatch(search, prod):
    if search.lower() in prod.description.lower() or search in prod.product_name.lower() or search in prod.brand.brand_name.lower():
        return True
    else:
        return False

def checkBrand(brandid, prod):
    if prod.brand_id == int(brandid):
        return True
    else:
        return False

def search(request):
    current_user = request.user
    customer = []
    try:
        customer = Customer.objects.get(user_id=current_user)
    except:
        pass

    search = request.GET['search']
    products = []
    brandid = 0

    try:
        brandid = request.GET['brand']
    except:
        pass

    allproducts = Products.objects.all()
    brands = Brands.objects.all()

    for products in allproducts:
        if brandid:
            products = [prod for prod in allproducts if searchMatch(search, prod) and checkBrand(brandid, prod)]
        else:
            products = [prod for prod in allproducts if searchMatch(search, prod)]

    n = len(products)

    current_user = request.user
    carts = Cart.objects.filter(user_id=current_user.id)
    qty = 0
    total = 0
    for cart in carts:
        total = total + cart.amount
        qty = qty + cart.qty

    params = {
        'customer': customer,
        'products': products,
        'n': n,
        'search': search.lower(),
        'brands': brands,
        'qty': qty,
        'total':total,
        'carts':carts,
    }
    return render(request, 'Buyer/search.html', params)



def productdetails(request, prid):
    current_user = request.user
    try:
        product = Products.objects.get(id=prid)
    except Products.DoesNotExist:
        return HttpResponseNotFound("Product does not exist")

    carts = Cart.objects.filter(user_id=current_user.id)

    customer = None
    try:
        customer = Customer.objects.get(user_id=current_user.id)
    except Customer.DoesNotExist:
        pass

    pr_qty = 0
    try:
        pr_qty = Cart.objects.get(user_id=current_user.id, product_id=prid).qty
    except Cart.DoesNotExist:
        pass

    desc = product.product_desc
    descs = desc.split("#")

    qty = sum(cart.qty for cart in carts)
    total = sum(cart.amount for cart in carts)

    details = {
        'customer': customer,
        'product': product,
        'descs': descs,
        'qty': qty,
        'total': total,
        'carts': carts,
        'pr_qty': pr_qty
    }
    
    return render(request, 'Buyer/productdetail.html', details)




@login_required(login_url='/login')
def addtocart(request, prid):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    check_product = Cart.objects.filter(user_id=current_user.id, product_id=prid)
        
    if check_product:
        control = 1
    else:
        control = 0
    
    if control == 1:
        data = Cart.objects.get(user_id=current_user.id, product_id=prid)
        data.qty = data.qty + 1
        data.save()
    else:
        data = Cart()
        data.user_id = current_user.id
        data.product_id = prid
        data.qty = 1
        data.save()
    messages.success(request, data.product.product_name + " added to the Cart.")
    return HttpResponseRedirect(url)

def deletefromcart(request, prid):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product = Cart.objects.get(user_id=current_user.id, product_id=prid)
        
    if product.qty == 1:
        product.delete()
    else:
        product.qty = product.qty - 1
        product.save()
    
    messages.success(request, product.product.product_name + " deleted from the Cart.")
    return HttpResponseRedirect(url)



@login_required(login_url='/login')
def cart(request):
    current_user = request.user
    customer = Customer.objects.get(user_id=current_user.id)
    carts = Cart.objects.filter(user_id=current_user.id)

    total = 0
    qty = 0
    for cart in carts:
        total = total + cart.amount
        qty = qty + cart.qty
    
    cart_context = {
        'customer': customer,
        'carts': carts,
        'qty': qty,
        'total': total,
    }

    return render(request, 'Buyer/cart.html', cart_context)

    


def clearcart(request):
    current_user = request.user
    Cart.objects.filter(user_id=current_user.id).delete()
    return HttpResponseRedirect('/cart')



@login_required(login_url='/login')
def checkout(request):
    current_user = request.user
    carts = Cart.objects.filter(user_id=current_user.id)
    customer = Customer.objects.get(user_id=current_user.id)
    my_user = User.objects.get(id=current_user.id)

    total = sum(cart.amount for cart in carts)
    qty = sum(cart.qty for cart in carts)
    
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']

            order = Orders(
                user_id=current_user.id,
                first_name=firstname,
                last_name=lastname,
                mobile=mobile,
                city=city,
                state=state,
                total=total,
            )
            order.save()

            for cart in carts:
                order_product = OrderProduct(
                    order_id=order.id,
                    user_id=current_user.id,
                    product_id=cart.product_id,
                    qty=cart.qty,
                    price=cart.product.price,
                    amount=cart.amount
                )
                order_product.save()

            Cart.objects.filter(user_id=current_user.id).delete()
            messages.success(request, "Order has been placed. Thank You 😊")
            return redirect('ShopHome')
    else:
        form = CheckoutForm(initial={'first_name': my_user.first_name, 'last_name': my_user.last_name})

    details = {
        'myuser': my_user,
        'customer': customer,
        'carts': carts,
        'qty': qty,
        'total': total,
        'form': form
    }

    return render(request, 'Buyer/checkout.html', details)




@login_required(login_url='/login')
def updateProfile(request):
    user = request.user
    
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('/login')
    else:
        form = UpdateProfileForm(initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    
    return render(request, 'Buyer/updateprofile.html', {'form': form})
