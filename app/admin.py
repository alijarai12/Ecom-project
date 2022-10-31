from django.contrib import admin
from .models import  Product, Category, Cart, Order

# Register your models here.
@admin.register(Category)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','category_name']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','description', 'price', 'product_image', 'created_at']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'product', 'quantity', 'status','payment_method', 'ordered_date']


#customizing admin panel
admin.site.site_header = "Ecom"
admin.site.index_title = "E-Shopping"
admin.site.site_title = "E-Shopping Dashboard"