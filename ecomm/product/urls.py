from django.urls import path
from product.views import get_products , add_to_cart

urlpatterns = [
   path('<slug>/', get_products , name="get_products"),
   path('<uid>/', add_to_cart , name="add_to_cart"),
   

]