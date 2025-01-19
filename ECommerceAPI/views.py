from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import MenuItems, Cart
from .serializers import MenuItemSerializer, CartSerializer
from .custom_permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User, Group


class StandardResultsPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 100


class MenuItemsViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for handling MenuItems with filtering, searching, ordering, and pagination.
    """

    queryset = MenuItems.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]  # Default permissions
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ["price", "title", "category"]  # Fields to filter by
    ordering_fields = ["price", "id"]  # Fields to order by
    search_fields = ["title", "category"]  # Fields to search by
    pagination_class = StandardResultsPagination

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


class ManagerAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        manager_group = Group.objects.get(name="Manager")
        manager = manager_group.user_set.all()
        data = [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in manager
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)
        manager_group = Group.objects.get(name="Manager")
        manager_group.user_set.add(user)
        return Response(
            {"message": f"User {user.username} added to the manager group"},
            status=status.HTTP_201_CREATED,
        )


class ManagerDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]
        return [permissions.IsAuthenticated()]

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        manager_group = Group.objects.get(name="Manager")
        if user in manager_group.user_set.all():
            manager_group.user_set.remove(user)
            return Response(
                {"message": f"User {user.username} remove from the manager group"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "User not found in manager group"},
            status=status.HTTP_404_NOT_FOUND,
        )


class ManagerDeliveryCrewView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        delivery_crew = Group.objects.get(name="DeliveryCrew")
        delivery_boys = delivery_crew.user_set.all()
        data = [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in delivery_boys
        ]
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)
        manager_group = Group.objects.get(name="DeliveryCrew")
        manager_group.user_set.add(user)
        return Response(
            {"message": f"User {user.username} added to the Delivery Crew group"},
            status=status.HTTP_201_CREATED,
        )


class ManagerDeliveryCrewDetailView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]
        return [permissions.IsAuthenticated()]

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        manager_delivery_group = Group.objects.get(name="Delivery Crew")
        if user in manager_delivery_group.user_set.all():
            manager_delivery_group.user_set.remove(user)
            return Response(
                {
                    "message": f"User {user.username} remove from the Delivery Crew group"
                },
                status=status.HTTP_200_OK,
            )
