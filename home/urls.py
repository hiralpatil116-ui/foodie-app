from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =====================================================
    # NORMAL MENU
    # =====================================================

    path(
        "menu/",
        views.menu,
        name="menu"
    ),


    # =====================================================
    # JAIN MENU
    # =====================================================

    path(
        "jain-menu/",
        views.jain_menu,
        name="jain_menu"
    ),


    # =====================================================
    # CART
    # =====================================================

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    # =====================================================
    # Admin-Dashboard
    # =====================================================

    path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
),

    # =====================================================
    # ADD TO CART
    # =====================================================

    path(
        "add-to-cart/<int:food_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),


    # =====================================================
    # QUANTITY
    # =====================================================

    path(
        "cart/increase/<int:food_id>/",
        views.increase_quantity,
        name="increase_quantity"
    ),

    path(
        "cart/decrease/<int:food_id>/",
        views.decrease_quantity,
        name="decrease_quantity"
    ),


    # =====================================================
    # REMOVE FROM CART
    # =====================================================

    path(
        "cart/remove/<int:food_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),


    # =====================================================
    # CHECKOUT
    # =====================================================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    # =====================================================
    # PLACE ORDER
    # =====================================================

    path(
        "place-order/",
        views.place_order,
        name="place_order"
    ),


    # =====================================================
    # ORDER SUCCESS
    # =====================================================

    path(
        "order-success/<int:order_id>/",
        views.order_success,
        name="order_success"
    ),


    # =====================================================
    # MY ORDERS
    # =====================================================

    path(
        "my-orders/",
        views.my_orders,
        name="my_orders"
    ),


    # =====================================================
    # cancel ORDERS
    # =====================================================

    path(
    "cancel-order/<int:order_id>/",
    views.cancel_order,
    name="cancel_order"
),

    # =====================================================
    # CONTACT
    # =====================================================

    path(
        "contact/",
        views.contact,
        name="contact"
    ),


    # =====================================================
    # REGISTER
    # =====================================================

    path(
        "register/",
        views.register,
        name="register"
    ),


    # =====================================================
    # LOGIN
    # =====================================================

    path(
        "login/",
        views.login_view,
        name="login"
    ),


    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),





]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)


path('payment/success/', views.payment_success, name='payment_success'),
path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
