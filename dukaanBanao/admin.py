from django.contrib import admin
from .models import account, image, store, product

# Register your models here.

admin.site.register(account)
admin.site.register(store)
admin.site.register(product)
admin.site.register(image)