from dataclasses import field
from math import prod
from unittest.util import _MAX_LENGTH
from importlib_metadata import requires
from rest_framework import serializers
from .models import account, category, customer, image, order, product, store


class customerIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = customer
        fields = ["id"]

class storeIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = store
        fields = ["id"]

class accountIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ["id"]

class productIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ["id"]

class accountSerializer(serializers.ModelSerializer):
    '''
    Creates serialization i.e. conversion of models to string and string to model for data exchange

    Args:
        object(obj): obj of type account from models.py

    returns:
        serialized value
    '''
    name = serializers.CharField(max_length=20, required=True)
    phNumber = serializers.DecimalField(required=True, decimal_places=0, max_value=9999999999, min_value=1000000000, max_digits=10)
    otp = serializers.DecimalField(required=True, decimal_places=0, max_value=9999, min_value=1000, max_digits=4)
    token = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = account
        fields = ("__all__")



class storeSerializer(serializers.ModelSerializer):
    storeName= serializers.CharField(max_length=10, required=True)
    address = serializers.CharField(max_length=50, required=True)
    storeURL = serializers.URLField(max_length=50, required=False)
    account_ID = serializers.IntegerField(required=False)
    product_ID = serializers.SerializerMethodField()

    class Meta:
        model = store
        fields = ["storeName", "address", "storeURL", "account_ID", "product_ID"]

    def get_account_ID(self, obj):
        return accountIDSerializer(obj.account_ID).data

    def get_product_ID(self, obj):
        return productIDSerializer(obj.product_ID.all(), many=True).data

class storeSerializerGET(serializers.ModelSerializer):
    storeName= serializers.CharField(max_length=10, required=True)
    address = serializers.CharField(max_length=50, required=True)
    storeURL = serializers.URLField(max_length=50, required=False)
    account_ID = serializers.SerializerMethodField(required=False)
    product_ID = serializers.SerializerMethodField()

    class Meta:
        model = store
        fields = ["storeName", "address", "storeURL", "account_ID", "product_ID"]

    def get_account_ID(self, obj):
        return accountIDSerializer(obj.account_ID).data

    def get_product_ID(self, obj):
        return productIDSerializer(obj.product_ID.all(), many=True).data

class imageSerializer(serializers.ModelSerializer):
    # img = serializers.ImageField()
    class Meta:
        model = image
        fields = ["img"]

class productSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = product
        fields = ["productName", "description", "MRP", "image", "SP", "cat"]

    def get_image(self, obj):
        return imageSerializer(obj.image.all(), many=True).data

    # def get_category(self, obj):
    #     return categorySerializer(obj.categoryName).data
    


class categorySerializer(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField()
    
    class Meta:
        model = category
        fields = ["categoryName", "product_id"]

    def get_product_id(self, obj):
        return productSerializer(obj.product_id.all(), many=True).data


class customerSerializer(serializers.ModelSerializer):
    '''
    Creates serialization i.e. conversion of models to string and string to model for data exchange

    Args:
        object(obj): obj of type account from models.py

    returns:
        serialized value
    '''
    phNumber = serializers.DecimalField(required=True, decimal_places=0, max_value=9999999999, min_value=1000000000, max_digits=10)
    otp = serializers.DecimalField(required=True, decimal_places=0, max_value=9999, min_value=1000, max_digits=4)
    token = serializers.CharField(max_length=500, required=False)

    class Meta:
        model = customer
        fields = ("__all__")

class orderSerializer(serializers.ModelSerializer):
    customer_ID = serializers.IntegerField(required=False)
    product_ID = serializers.IntegerField(required=False)
    store_ID = serializers.IntegerField(required=False)

    class Meta:
        model = order
        fields = ["customer_ID", "product_ID", "store_ID", "quantity"]

    def get_customer_ID(self, obj):
        return customerIDSerializer(obj.customer_ID).data

    def get_product_ID(self, obj):
        return productIDSerializer(obj.product_ID).data

    def get_store_ID(self, obj):
        return storeIDSerializer(obj.store_ID).data


class cartSerializer(serializers.ModelSerializer):
    customer_ID = serializers.IntegerField(required=False)
    product_ID = serializers.IntegerField(required=False)
    store_ID = serializers.IntegerField(required=False)

    class Meta:
        model = order
        fields = ["customer_ID", "product_ID", "store_ID", "quantity"]

    def get_customer_ID(self, obj):
        return customerIDSerializer(obj.customer_ID).data

    def get_product_ID(self, obj):
        return productIDSerializer(obj.product_ID).data

    def get_store_ID(self, obj):
        return storeIDSerializer(obj.store_ID).data

class storeViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = store
        fields = ["storeName", "address", "id"]
