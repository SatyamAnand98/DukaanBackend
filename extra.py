    # def get(self, request):
    #     if "id" in request.data:
    #         id = request.data["id"]
    #     if "id" in request.data:
    #         item = User.objects.get(id=id)
    #         serializer = UserSerializer(item)
    #         return Response(
    #             {
    #                 "status": "success",
    #                 "data": serializer.data,
    #             },
    #             status=status.HTTP_200_OK
    #         )
    #     if "id" not in request.data:
    #         items = User.objects.all()
    #         serializer = UserSerializer(items, many=True)
    #         return Response(
    #             {
    #                 "status": "success",
    #                 "data": serializer.data
    #             },
    #             status=status.HTTP_200_OK
    #         )