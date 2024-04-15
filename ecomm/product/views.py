
from django.shortcuts import render , redirect
from product.models import product
from accounts.models import Cart , CartItems
from product.models import SizeVariant
from django.http import HttpResponseRedirect



def get_products(request , slug):
   
    try:
        Product = product.objects.get(slug =slug)
        context = {'product' : Product }
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = Product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
            print(price)
        return render(request  , 'product/product.html' , context = context)

    except Exception as e:
        print(e)



def add_to_cart(request , uid):
     variant = request.GET.get('variant')
     Product = product.objects.get(uid = uid)
     user = request.user
     cart , _ = Cart.objects.get_or_create(user = user , is_paid = False)
     cart_items = CartItems.objects.create(cart=cart, Product=Product)
     if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_items.size_variant = size_variant
        cart_items.save()

     return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

