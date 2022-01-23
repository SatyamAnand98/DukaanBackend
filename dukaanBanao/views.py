import re
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import account, image, product, store
from rest_framework import status
from .serializers import accountSerializer, productSerializer, storeSerializer
import jwt
from secrets import token_urlsafe
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

############################ HELPER #####################################
def modify_input_for_multiple_files(productName, description, MRP, image):
    dict = {}
    dict['productName'] = productName
    dict['description'] = description
    dict['MRP'] = MRP
    dict['image'] = image
    return dict
#########################################################################

class accountAPIView(APIView):
    def post(self, request):
        serializer = accountSerializer(data=request.data)
        if serializer.is_valid():
            jwToken = jwt.encode(
                {
                    "phoneNumber": serializer.data["phNumber"],
                    "otp": serializer.data["otp"]
                },
                'MySecretKey',
                algorithm='HS256'
            )
            acc = account(
                name = serializer.data['name'],
                phNumber = serializer.data['phNumber'],
                otp = serializer.data["otp"],
                token = jwToken
            )
            acc.save()
            # serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": {
                        "User ID": acc.id,
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
        serializer = storeSerializer(data=request.data)
        account_id = account.objects.get(token=request.headers["Token"])
        if serializer.is_valid() and account_id:
            randomURL = f"https://{serializer.data['storeName']}Dukaan.com/{token_urlsafe(8)}"
            Store = store(
                storeName = serializer.data["storeName"],
                address = serializer.data["address"],
                storeURL = randomURL,
                account_ID = account.objects.get(token=request.headers["Token"])
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
                        "error": serializer.errors,
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
                serializer = storeSerializer(item)
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
        serializer = storeSerializer(items, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

###########################################################################################################


# class productAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
    
#     def get(self, request):
#         all_products = product.objects.all()
#         serializer = productSerializer(all_products, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     def post(self, request, *args, **kwargs):
#         productName = request.data["productName"]
#         description = request.data["description"]
#         MRP = request.data["MRP"]
#         images = dict((request.data).lists())['image']
        
#         flag = 1
#         arr = []

#         for img_name in images:
#             modified_data = modify_input_for_multiple_files(productName, description, MRP, img_name)
#             file_serializer = productSerializer(data=modified_data)
#             if file_serializer.is_valid():
#                 file_serializer.save()
#                 arr.append(file_serializer.data)
#             else:
#                 flag = 0

#         if flag == 1:
#             return Response(
#                 {
#                     "status": "success",
#                     "data": arr
#                 },
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 {
#                     "status": "error",
#                     "data": arr
#                 },
#                 status=status.HTTP_400_BAD_REQUEST



class productAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request):
        all_products = product.objects.all()
        serializer = productSerializer(all_products, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        productName = request.data["productName"]
        description = request.data["description"]
        MRP = request.data["MRP"]
        images = dict((request.data).lists())['image']
        

        modified_data = modify_input_for_multiple_files(productName, description, MRP, images)
        file_serializer = productSerializer(data=modified_data)
        if file_serializer.is_valid():


            Product = product(
                productName = productName,
                description = description,
                MRP = MRP
            )

            Product.save()

            for im_age in images:
                print(im_age)
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
        else:
            return Response(
                {
                    "status": "error",
                    "data": "error"
                },
                status=status.HTTP_400_BAD_REQUEST
            )