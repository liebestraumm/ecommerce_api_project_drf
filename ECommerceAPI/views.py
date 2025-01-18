from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from .models import MenuItems, Cart
from .serializers import MenuItemSerializer, CartSerializer
from .custom_permissions import *


# Create your views here.
class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        """
        Override to allow only managers to create or modify menu items.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsManager()]
        return [permissions.IsAuthenticated()]

    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartmanagementView(generics.ListCreateAPIView, generics.DestroyAPIView):

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Pass the current user to the serializer
        menuitem = self.request.data.get("menuitem")
        if Cart.objects.filter(menuitem=menuitem):
            return Response({"message": "Item Alredy Exist in Cart "})
        else:
            serializer.save(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        user_cart = self.get_queryset()
        count = user_cart.count()
        if count > 0:
            user_cart.delete()
            return Response(
                {"message": f"Deleted {count} items from the cart."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Cart is already empty."}, status=status.HTTP_200_OK
        )
