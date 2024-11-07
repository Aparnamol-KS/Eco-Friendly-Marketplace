from django.contrib import admin
from .models import Product,Order,Eco_certifications,Cart,Wishlist,UserProfile,orderedItems
from import_export.admin import ImportExportModelAdmin

# Register your models here.
 

# Register the model with the Django admin site

admin.site.register(Order)
admin.site.register(Eco_certifications)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(UserProfile)
admin.site.register(orderedItems)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('product_name', 'price', 'category', 'stock')
    search_fields = ('product_name', 'category')
