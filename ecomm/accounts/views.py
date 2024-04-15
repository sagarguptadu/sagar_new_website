from django.shortcuts import render ,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth import authenticate , login , logout
from .models import profile ,Cart ,CartItems 
from product.models import product
from product.models import SizeVariant


# Create your views here.
def login_page(request):
    if request.method == 'POST':
        
        email =request.POST.get('email')
        password =request.POST.get('password')


        user_obj= User.objects.filter(username= email)

        if not user_obj.exists():
          messages.error(request, 'Account not found.')
          return HttpResponseRedirect(request.path_info)
        
        if  not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'your account is not verified.')
            return HttpResponseRedirect(request.path_info)
           
        user_obj = authenticate(username = email , password = password)
        if user_obj:
           login(request , user_obj)
           return redirect('/')
        messages.success(request , 'Invalid credentials .')
        return HttpResponseRedirect(request.path_info)

    return render(request , 'accounts/login.html')

def register_page(request):
    if request.method == 'POST':
        first_name =request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        email =request.POST.get('email')
        password =request.POST.get('password')


        user_obj= User.objects.filter(username= email)

        if user_obj.exists():
          messages.error(request, 'email is already  taken.')
          return HttpResponseRedirect(request.path_info)
        
        print(email)



        user_obj= User.objects.create(first_name = first_name , last_name = last_name , email= email , username = email)
        user_obj.set_password(password) 
        user_obj.save()

        messages.success(request , 'An email has been sent on your mail .')
        return HttpResponseRedirect(request.path_info)

    return render(request , 'accounts/register.html')

def activate_email(request , email_token):
   try:
      user = profile.obects.get(email_token = email_token)
      user.is_email_verified = True
      user.save()
      return redirect('/')  
   except Exception as e:
      return HttpResponse('Invalid email token.')
   

def add_to_cart(request , uid):
     variant = request.GET.get('variant')
     Product = product.objects.get(uid = uid)
     user = request.user
     cart , _ = Cart.objects.get_or_create(user = user , is_paid = False)
     cart_item = CartItems.objects.create(cart=cart, Product=Product)
     if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_item.size_variant = size_variant
        cart_item.save()

     return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request , cart_item_uid ):
   try:
      cart_item =CartItems.objects.get(uid = cart_item_uid)
      cart_item.delete()
   except Exception as e:
      print(e)
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  




def cart(request):
   context = {'cart' : Cart.objects.get(is_paid=False, user= request.user)}
   return render(request , 'accounts/cart.html' , context)
 

    