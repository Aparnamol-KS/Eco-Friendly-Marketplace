from django.contrib import admin
from .models import UserDetails,Product,Order,Eco_certifications,Cart,Wishlist
from import_export.admin import ImportExportModelAdmin

# Register your models here.
 

# Register the model with the Django admin site
admin.site.register(UserDetails)
admin.site.register(Order)
admin.site.register(Eco_certifications)
admin.site.register(Cart)
admin.site.register(Wishlist)

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ('product_name', 'price', 'category', 'stock')
    search_fields = ('product_name', 'category')
