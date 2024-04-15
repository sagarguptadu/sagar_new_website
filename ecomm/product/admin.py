from csv import list_dialects
from django.contrib import admin

# Register your models here.

from .models import *




admin.site.register(category)

class ProductImageAdmin(admin.StackedInline):
    model = productimage

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name' , 'price' ]
    inlines = [ProductImageAdmin]


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    list_display = ['color_name' , 'price']
    model = ColorVariant

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name' , 'price']

    model = SizeVariant


admin.site.register(product ,ProductAdmin)


admin.site.register(productimage)