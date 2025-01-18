from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["id", "slug", "title"]


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = models.MenuItems
        fields = ["id", "title", "price", "featured", "category", "category_id"]


class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(
        queryset=models.MenuItems.objects.all()
    )

    class Meta:
        model = models.Cart
        fields = ["id", "menuitem", "quantity", "unit_price", "price", "user"]
        read_only_fields = ["id", "user", "unit_price", "price"]

    def create(self, validated_data):
        # Calculate price and unit_price
        menuitem = validated_data["menuitem"]
        quentity = validated_data["quantity"]

        validated_data["unit_price"] = menuitem.price
        validated_data["price"] = menuitem.price * quentity

        # Save the Cart object
        return super().create(validated_data)
