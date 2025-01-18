from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"menu-items", MenuItemsViewSet, basename="menu-items")

urlpatterns = [
    path("cart/menu-items", CartmanagementView.as_view(), name="cart/menu-items"),
    *router.urls,
]
