from django.contrib import admin
from .models import (
    CustomerProfile,
    SellerProfile,
    Store,
    Product,
    CartItem,
    Order,
    OrderItem,
)


admin.site.register(CustomerProfile)
admin.site.register(SellerProfile)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)