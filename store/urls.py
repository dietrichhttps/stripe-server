from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:id>/', views.buy_item, name='buy_item'),
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('buy/order/<int:id>/', views.buy_order, name='buy_order'),
    path('item/order/<int:id>/', views.order_detail, name='order_detail'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
