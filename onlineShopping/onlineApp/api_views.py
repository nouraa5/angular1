from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import AddProductFormSerializer
from .forms import AddProductForm
from django.contrib.auth.models import User
from .models import Brands
from .models import Products as Product
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


class AddProductFormView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        form = AddProductForm()
        form_data = {
            'product_name': form['product_name'].value() or '',
            'product_desc': form['product_desc'].value() or '',
            'brand': form['brand'].value() or '',
            'product_price': form['product_price'].value() or '',
            'product_image': form['product_image'].value() or '',
        }
        form_serializer = AddProductFormSerializer(data=form_data)
        form_serializer.is_valid(raise_exception=False)
        response_data = {
            'initial_data': form_serializer.initial_data,
            'choices': {
                'brand': [{'code': bt.brand_type, 'title': bt.brand_title} for bt in Brands.objects.all()],
            }
        }
        print(request.user)
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        files = request.FILES.get('product_image')
        print(data)
        # print(request.user)
        if files:
            data['product_image'] = files
        print(data['product_name'])
        form_serializer = AddProductFormSerializer(data=data)
        if form_serializer.is_valid():
            # print(form_serializer.errors)
            type = Brands.objects.get(brand_type=data['brand'])
            # seller = User.objects.get(username='Ali')
            seller = request.user
            product = Product(product_name=data['product_name'], brand=type,
                              product_desc=data['product_desc'], seller=seller, product_price=data['product_price'], product_image=data['product_image'])
            print(product)
            product.save()
            return Response({'message': 'Product added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def search_product(request):
    if request.method == 'GET':
        brands = Brands.objects.all()
        data = {
            'brands': [{'brand_type': bt.brand_type, 'brand_title': bt.brand_title} for bt in brands],
        }
        print(data)
        return JsonResponse(data)

    elif request.method == 'POST':
        data = json.loads(request.body)
        brand_code = data.get('brand')
        print(data)
        print(brand_code)
        products = Product.objects.filter(
            brand=brand_code)
        products_data = [{
            'product_id': product.product_id,
            'seller_name': product.seller.username,
            'product_name': product.product_name,
            'product_desc': product.product_desc,
            'product_price': product.product_price,
            'product_image': request.build_absolute_uri(product.product_image.url) if product.product_image else None,
            'brand': product.brand.brand_title,
        } for product in products]
        print(products_data)
        return JsonResponse({'products': products_data})


@csrf_exempt
def get_myProducts(request, id):
    if request.method == 'GET':
        products = Product.objects.filter(seller=id)
        products_data = [{'product_id': product.product_id,
                          'seller_name': product.seller.username,
                          'product_name': product.product_name,
                          'product_desc': product.product_desc,
                          'product_price': product.product_price,
                          'product_image': request.build_absolute_uri(product.product_image.url) if product.product_image else None,
                          'brand': product.brand.brand_type,
                          } for product in products]
        return JsonResponse({'products': products_data})


@api_view(['GET', 'POST'])
def edit_product(request, product_id):
    if request.method == 'GET':
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        products_data = {
            'product_id': product.product_id,
            'seller_name': product.seller.username,
            'product_name': product.product_name,
            'product_desc': product.product_desc,
            'product_price': product.product_price,
            'product_image': request.build_absolute_uri(product.product_image.url) if product.product_image else None,
            'brand': product.brand.brand_type,
            'brands': [{'brand_type': st.brand_type, 'brand_title': st.brand_title} for st in Brands.objects.all()],
        }
        return JsonResponse({'product': products_data})

    elif request.method == 'POST':
        product = Product.objects.get(product_id=product_id)

        product_name = request.POST.get(
            'product_name', product.product_name)
        product_desc = request.POST.get('product_desc', product.product_desc)
        product_price = request.POST.get('product_price', product.product_desc)
        brand_title = request.POST.get(
            'brand', product.brand.brand_title)
        product_image = request.FILES.get('product_image', product.product_image)

        try:
            brand_instance = Brands.objects.get(
                type_title=brand_title)
        except Brands.DoesNotExist:
            return JsonResponse({'error': 'Invalid product type'}, status=status.HTTP_400_BAD_REQUEST)

        product.product_name = product_name
        product.product_desc = product_desc
        product.product_price = product_price
        product.brand = brand_instance
        product.product_image = product_image
        product.save()

        return Response({'message': 'Product updated successfully'}, status=status.HTTP_200_OK)


@require_http_methods(["GET"])
def user_info(request):
    user_id = request.GET.get('user_id')
    print(f"Received user_id: {user_id}")  # Debugging statement

    if not user_id:
        return JsonResponse({'error': 'User ID not provided'}, status=400)

    try:
        user = User.objects.get(id=user_id)
        print(f"User found: {user}")  # Debugging statement
    except User.DoesNotExist:
        print("User not found")  # Debugging statement
        return JsonResponse({'error': 'User not found'}, status=404)

    user_data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return JsonResponse(user_data)

@api_view(['DELETE'])
def delete_product(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_product_name(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
        return Response({'title': product.product_name}, status=status.HTTP_200_OK)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_profile(request):
    user_id = request.query_params.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        user_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }
        return Response({'user': user_data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_user_profile(request):
    user_id = request.query_params.get('user_id')
    data = request.data
    print(data)
    try:
        user = User.objects.get(id=user_id)
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()
        return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
