from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddProductForm, EditProfileForm, SearchForm
from .models import Brands, Products
from django.contrib import messages


def add_product(request):
    if not request.user.groups.filter(name='Seller').exists():
        return redirect('/')
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('/sell/my_products')
        else:
            messages.error(request, 'Form submission failed. Please check the data entered.')
    else:
        form = AddProductForm()
    return render(request, 'onlineApp/add_products.html', {'form': form})


def my_products(request):
    if not request.user.groups.filter(name='Seller').exists():
        return redirect('/')
    user_products = Products.objects.filter(seller=request.user)
    return render(request, 'onlineApp/my_products.html', {'products': user_products})



def edit_product(request, product_id):
    if not request.user.groups.filter(name='Seller').exists():
        return redirect('/')
    try:
        product = Products.objects.get(product_id=product_id)
        if product.seller != request.user:
            return redirect('/')
        if request.method == 'POST':
            form = AddProductForm(
                request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('/sell/my_products')
        else:
            form = AddProductForm(instance=product)
        return render(request, 'onlineApp/edit_products.html', {'form': form})
    except Products.DoesNotExist:
        return redirect('/')


def delete_product(request, product_id):
    if not request.user.groups.filter(name='Seller').exists():
        return redirect('/')
    products = get_object_or_404(Products, product_id=product_id)
    if products.seller != request.user:
        return redirect('/')
    if request.method == 'POST':
        if products.product_image:
            products.product_image.delete()
        products.delete()
        return redirect('/sell/my_products')
    return render(request, 'onlineApp/delete_product_confirm.html', {'products': products})



def edit_profile(request):
    user = request.user
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            return redirect('/')
    else:
        form = EditProfileForm(initial={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })
    
    return render(request, 'onlineApp/edit_profile.html', {'form': form})


def search_product(request):
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            brand = form.cleaned_data['brand_title']
            custom_text = form.cleaned_data['custom_text']
            products = Products.objects.filter(brand=brand)
            if custom_text:
                products = products.filter(product_name=custom_text)
            return render(request, 'onlineApp/search_results.html', {'products': products, 'form': form})
    else:
        brands = Brands.objects.all()
        return render(request, 'onlineApp/search_products.html', {'brands': brands, 'form': form})


# def view_profile(request):
#     if request.user.is_authenticated:
#         user = request.user
#         return render(request, 'onlineApp/view_profile.html', {'user': user})
#     else:
#         return redirect('/')  
