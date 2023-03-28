from django.urls import path
from . import views

urlpatterns = [
    path('groups/manager/users', views.managers),
    path('groups/delivery-crew/users', views.delivery_crew),
    path('menu-items', views.menu_items),
    path('menu-items/<int:menu_item_id>', views.single_menu_item),
    path('cart/menu-items', views.cart_items),
    path('orders', views.orders),
    path('orders/<int:order_id>', views.orders),
]