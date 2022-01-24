from importlib.abc import ResourceReader
import re
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import account, cart, category, customer, image, order, product, store
from rest_framework import status
from .serializers import accountSerializer, cartSerializer, categorySerializer, customerSerializer, orderSerializer, productSerializer, storeSerializer, storeSerializerGET, storeViewSerializer
import jwt
from secrets import token_urlsafe
from rest_framework.parsers import MultiPartParser, FormParser
from .helper import modify_input_for_product_model, modify_input_for_category_model
from dukaanBanao import serializers


# Create your views here.

class accountAPIView(APIView):
    def post(self, request):
        jwToken = jwt.encode(
                {
                    "phoneNumber": request.data["phNumber"],
                    "otp": request.data["otp"]
                },
                'MySecretKey',
                algorithm='HS256'
            )
        request.data["token"] = jwToken
        serializer = accountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": {
                        "User ID": serializer.data["id"],
                        "Token": jwToken
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "error",
                    "data": {
                        "error": serializer.errors,
                        "error_message": serializer.error_messages
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, id=None):
        check = account.objects.filter(id=id).exists()
        if id:
            if check:
                item = account.objects.get(id=id)
                serializer = accountSerializer(item)
                return Response(
                    {
                        "status": "success",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "status": "error",
                        "data": "id does not exist in database"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
                
        items = account.objects.all()
        serializer = accountSerializer(items, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class storeAPIView(APIView):
    def post(self, request):
        account_id = account.objects.get(token=request.headers["Token"])
        if account_id:
            randomURL = f"https://{request.data['storeName']}Dukaan.com/{token_urlsafe(8)}"
            Store = store(
                storeName = request.data["storeName"],
                address = request.data["address"],
                storeURL = randomURL,
                account_ID = account_id
            )

            Store.save()

            return Response(
                {
                    "status": "success",
                    "data": {
                        "User ID": Store.id,
                        "Token": randomURL
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "error",
                    "data": {
                        "error": "serializer.errors",
                        "error_message": "user with this token does not exist"
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, id=None):
        check = store.objects.filter(id=id).exists()
        if id:
            if check:
                item = store.objects.get(id=id)
                serializer = storeSerializerGET(item)
                return Response(
                    {
                        "status": "success",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "status": "error",
                        "data": "id does not exist in database"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
                
        items = store.objects.all()
        serializer = storeSerializerGET(items, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )



class productAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        all_products = product.objects.all()
        serializer = productSerializer(all_products, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):

        try:
        
            images = dict((request.data).lists())['image']

            product_data = modify_input_for_product_model(
                request.data["productName"], 
                request.data["description"], 
                request.data["MRP"], 
                images,
                request.data["SP"],
                request.data["category"]
            )
            Product = product(
                productName = product_data["productName"],
                description = product_data["description"],
                MRP = product_data["MRP"],
                SP = product_data["SP"],
                cat = product_data["category"]
            )

            Product.save()

        except Exception as e:
            pass


        if category.objects.filter(categoryName=request.data["category"]).exists():
            Category = category.objects.filter(categoryName=request.data["category"])[0]
            Category.product_id.add(Product)
            Category.save()
        else:
            Category = category(
                categoryName = request.data["category"],
            )

            Category.save()
            Category.product_id.add(Product)
            Category.save()

        try:
            Store = store.objects.filter(id=request.data["store_ID"])[0]
            Store.product_ID.add(Product)
            Store.save()
        except Exception as e:
            pass
        

        try:

            for im_age in images:
                Img = image(
                    img = im_age
                )
                Img.save()
                Product.image.add(Img)
            Product.save()

            

            return Response(
                {
                    "status": "success",
                    "data": images
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "data": e
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class categorisedView(APIView):
    def post(self, request):
        Store = store.objects.filter(id= request.data["store_ID"])[0]
        Store = storeSerializerGET(Store)
        product_list = Store.data["product_ID"]
        result = {}
        for i in product_list:
            Product = product.objects.filter(id = i["id"])[0]
            Category = productSerializer(Product)
            if Category.data["cat"] in result.keys():
                tempRes = {}
                tempRes["productName"] = Category.data["productName"]
                tempRes["description"] = Category.data["description"]
                tempRes["MRP"] = Category.data["MRP"]
                tempRes["image"] = Category.data["image"]
                tempRes["SP"] = Category.data["SP"]
                result[Category.data["cat"]].append(tempRes)
            else:
                tempRes = {}
                tempRes["productName"] = Category.data["productName"]
                tempRes["description"] = Category.data["description"]
                tempRes["MRP"] = Category.data["MRP"]
                tempRes["image"] = Category.data["image"]
                tempRes["SP"] = Category.data["SP"]
                result[Category.data["cat"]] = [tempRes]


        return Response(
            {
                "status": "success",
                "data": result
            },
            status=status.HTTP_200_OK
        )

class customerAPIView(APIView):
    def post(self, request):
        jwToken = jwt.encode(
                {
                    "phoneNumber": request.data["phNumber"],
                    "otp": request.data["otp"]
                },
                'MySecretKey',
                algorithm='HS256'
            )
        request.data["token"] = jwToken
        serializer = customerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": {
                        "User ID": serializer.data["id"],
                        "Token": jwToken
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    "status": "error",
                    "data": {
                        "error": serializer.errors,
                        "error_message": serializer.error_messages
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, id=None):
        check = customer.objects.filter(id=id).exists()
        if id:
            if check:
                item = customer.objects.get(id=id)
                serializer = customerSerializer(item)
                return Response(
                    {
                        "status": "success",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "status": "error",
                        "data": "id does not exist in database"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
                
        items = customer.objects.all()
        serializer = customerSerializer(items, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


class orderView(APIView):

    def post(self, request):
        customer_id = customer.objects.get(id=request.data["customer_ID"])
        product_id = product.objects.get(id=request.data["product_ID"])
        store_id = store.objects.get(id=request.data["store_ID"])
        Store = store.objects.filter(id=request.data["store_ID"])[0]
        Store = storeSerializerGET(Store)
        flag = 0
        product_list = Store.data["product_ID"]
        temp_list = []
        for i in product_list:
            temp_list.append(i["id"])
        
        if product_id.id in temp_list:
            flag = 1

        serializer = orderSerializer(data=request.data)
        if customer_id and product_id and store_id and flag and serializer.is_valid():
            Order = order(
                customer_ID = customer_id,
                product_ID = product_id,
                store_ID = store_id,
                quantity = request.data['quantity']
            )
            Order.save()
            # serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

class cartView(APIView):

    def post(self, request):
        customer_id = customer.objects.get(id=request.data["customer_ID"])
        product_id = product.objects.get(id=request.data["product_ID"])
        store_id = store.objects.get(id=request.data["store_ID"])
        Store = store.objects.filter(id=request.data["store_ID"])[0]
        Store = storeSerializerGET(Store)
        flag = 0
        product_list = Store.data["product_ID"]
        temp_list = []
        for i in product_list:
            temp_list.append(i["id"])
        
        if product_id.id in temp_list:
            flag = 1

        serializer = cartSerializer(data=request.data)
        if customer_id and product_id and store_id and flag and serializer.is_valid():
            Cart = cart(
                customer_ID = customer_id,
                product_ID = product_id,
                store_ID = store_id,
                quantity = request.data['quantity']
            )
            Cart.save()
            # serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": serializer.data
                },
                status=status.HTTP_200_OK
            )

class placeOrderAPIView(APIView):
    def post(self, request):
        cart_id = cart.objects.get(id=request.data["cart_id"])

        serializer = orderSerializer(data=cart_id)

        Product = cart_id.product_ID
        Customer = cart_id.customer_ID
        Store = cart_id.store_ID
        quantity = cart_id.quantity
        
        cart_id.delete()
        # cart_id.save()

        Cart = order(
            customer_ID = Customer,
            product_ID = Product,
            store_ID = Store,
            quantity = quantity
        )

        Cart.save()

        print(serializer.is_valid())
        return Response(
            {
                "status": "success",
                "data": Cart.id
            },
            status=status.HTTP_200_OK
        )

class StoreDisplayAPIView(APIView):
    def post(self, request):
        Store = store.objects.get(storeURL=request.data["URL"])
        serializer = storeViewSerializer(Store)
        return JsonResponse(serializer.data, safe=False)

