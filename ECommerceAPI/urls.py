from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"menu-items", MenuItemsViewSet, basename="menu-items")

urlpatterns = [
    path("groups/manager/users", ManagerAPIView.as_view(), name="manager-users"),
    path(
        "groups/manager/users/<int:pk>",
        ManagerDetailView.as_view(),
        name="manager-users",
    ),
    path(
        "groups/delivery-crew/users",
        ManagerDeliveryCrewView.as_view(),
        name="delivery-crew-users",
    ),
    path(
        "groups/delivery-crew/users/<int:pk>",
        ManagerDeliveryCrewDetailView.as_view(),
        name="delivery-crew-users",
    ),
    path("cart/menu-items", CartmanagementView.as_view(), name="cart/menu-items"),
    *router.urls,
]
