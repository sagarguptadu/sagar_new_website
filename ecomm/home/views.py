from django.shortcuts import render
from product.models import product



def index(request):

    context = {'products' : product.objects.all()}
    return render(request , 'home/index.html' , context)