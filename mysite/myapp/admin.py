from django.contrib import admin
from .models import Product

# Register your models here.

admin.site.site_header = "Buy & Sell Site"
admin.site.site_title = "Buy & Sell Site"
admin.site.index_title = "Welcome to Buy & Sell Site"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'desc', 'image', 'seller_name')
    list_filter = ('name', 'price', 'desc', 'image', 'seller_name')
    search_fields = ('name','desc')
    list_per_page = 25
    
    
    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)
    
    actions = ('set_price_to_zero',)
    list_editable = ('price','desc')
admin.site.register(Product, ProductAdmin)