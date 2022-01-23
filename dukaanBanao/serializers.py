from dataclasses import field
from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from .models import account, image, product, store

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

class accountIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = account
        fields = ["id"]


class storeSerializer(serializers.ModelSerializer):
    storeName= serializers.CharField(max_length=10, required=True)
    address = serializers.CharField(max_length=50, required=True)
    storeURL = serializers.URLField(max_length=50, required=False)
    account_ID = serializers.SerializerMethodField()

    class Meta:
        model = store
        fields = ("__all__")

    def get_account_ID(self, obj):
        return accountIDSerializer(obj.account_ID).data

class imageSerializer(serializers.ModelSerializer):
    img = serializers.ImageField()
    class Meta:
        model = image
        fields = ("__all__")

class productSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = product
        fields = ["productName", "description", "MRP", "image"]

    def get_image(self, obj):
        return imageSerializer(obj.image.all(), many=True).data