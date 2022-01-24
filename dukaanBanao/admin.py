from django.contrib import admin
from .models import account, cart, customer, image, order, store, product, category

# Register your models here.

admin.site.register(account)
admin.site.register(store)
admin.site.register(product)
admin.site.register(image)
admin.site.register(category)
admin.site.register(customer)
admin.site.register(order)
admin.site.register(cart)