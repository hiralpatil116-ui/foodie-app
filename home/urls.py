from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('jain-menu/', views.jain_menu, name='jain_menu'),
    path('cart/', views.cart, name='cart'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cart/add/<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:food_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:food_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]