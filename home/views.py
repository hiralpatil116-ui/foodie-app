# =========================================================
# VIEWS.PY - FOODIE
# Clean Complete Version
# =========================================================

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q,Sum,Count
from django.shortcuts import get_object_or_404, redirect, render

from .models import Food, Order, OrderItem,ContactMessage
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse


from django.conf import settings
from django.shortcuts import redirect, render
import stripe
from .models import Order

 
stripe.api_key = settings.STRIPE_SECRET_KEY




# =========================================================
# FOOD IMAGES
# =========================================================

FOOD_IMAGES = {

    "margherita pizza":
        "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=90",

    "margherita":
        "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=90",

    "farmhouse pizza":
        "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=90",

    "pizza":
        "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=90",

    "veg burger":
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=90",

    "burger":
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=90",

    "gulab jamun":
        "https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=90",

    "ice cream":
        "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?auto=format&fit=crop&w=900&q=90",

    "chocolate cake":
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=900&q=90",

    "red sauce pasta":
        "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=90",

    "white sauce pasta":
        "https://images.unsplash.com/photo-1645112411341-6c4fd023714a?auto=format&fit=crop&w=900&q=90",

    "pasta":
        "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=90",

    "noodles":
        "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=900&q=90",

    "momos":
        "https://images.unsplash.com/photo-1625220194771-7ebdea0b70b9?auto=format&fit=crop&w=900&q=90",

    "manchurian":
        "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=900&q=90",
}


# =========================================================
# CATEGORY IMAGES
# =========================================================

CATEGORY_IMAGES = {

    "Pizza":
        "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=900&q=90",

    "Burger":
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=90",

    "Indian":
        "https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=900&q=90",

    "Chinese":
        "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=900&q=90",

    "Pasta":
        "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?auto=format&fit=crop&w=900&q=90",

    "Dessert":
        "https://images.unsplash.com/photo-1551024506-0bccd828d307?auto=format&fit=crop&w=900&q=90",

    "Drinks":
        "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=90",
}


# =========================================================
# HELPER - ATTACH FOOD IMAGE
# =========================================================

def attach_food_images(foods):

    for food in foods:

        food_name = food.name.strip().lower()

        if food.image:
            food.image_url = food.image

        elif food_name in FOOD_IMAGES:
            food.image_url = FOOD_IMAGES[food_name]

        elif food.category in CATEGORY_IMAGES:
            food.image_url = CATEGORY_IMAGES[food.category]

        else:
            food.image_url = (
                "https://images.unsplash.com/"
                "photo-1504674900247-0877df9cc836"
                "?auto=format&fit=crop&w=900&q=90"
            )

    return foods


# =========================================================
# HOME
# =========================================================

def home(request):

    foods = Food.objects.filter(
        available=True
    ).exclude(
        category="Jain"
    )

    attach_food_images(foods)

    return render(
        request,
        "home.html",
        {
            "foods": foods
        }
    )


# =========================================================
# MAIN MENU
# =========================================================

def menu(request):

    # IMPORTANT:
    # Jain foods will NOT appear in Main Menu.

    foods = Food.objects.filter(
        available=True
    ).exclude(
        category="Jain"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    category = request.GET.get(
        "category",
        ""
    ).strip()


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if search:

        foods = foods.filter(
            Q(name__icontains=search) |
            Q(category__icontains=search) |
            Q(description__icontains=search)
        )


    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    if category:

        foods = foods.filter(
            category__iexact=category
        )


    # -----------------------------------------------------
    # FOOD IMAGES
    # -----------------------------------------------------

    attach_food_images(foods)


    # -----------------------------------------------------
    # MAIN MENU CATEGORIES
    # -----------------------------------------------------

    categories = (
        Food.objects
        .filter(available=True)
        .exclude(category="Jain")
        .values_list("category", flat=True)
        .distinct()
    )


    return render(
        request,
        "menu.html",
        {
            "foods": foods,
            "categories": [
                (value, value)
                for value in categories
            ],
            "category_images": CATEGORY_IMAGES,
            "selected_category": category,
            "search": search,
        }
    )


# =========================================================
# JAIN MENU
# =========================================================

def jain_menu(request):

    # Only Jain food

    foods = Food.objects.filter(
        available=True,
        category="Jain"
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()


    # -----------------------------------------------------
    # JAIN SEARCH
    # -----------------------------------------------------

    if search:

        foods = foods.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )


    # -----------------------------------------------------
    # JAIN FOOD IMAGES
    # -----------------------------------------------------

    attach_food_images(foods)


    # -----------------------------------------------------
    # JAIN CATEGORIES
    # -----------------------------------------------------

    categories = Food.objects.filter(
    available=True
).exclude(
    category__iexact="Jain "
).values_list(
    "category",
    flat=True
).distinct()


    return render(
        request,
        "jain_menu.html",
        {
            "foods": foods,
            "categories": [
                (value, value)
                for value in categories
            ],
            "search": search,
        }
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, food_id):
    food = get_object_or_404(
        Food,
        id=food_id,
        available=True
    )

    cart = request.session.get("cart", {})
    food_id_str = str(food.id)

    if food_id_str in cart:
        try:
            cart[food_id_str] = int(cart[food_id_str]) + 1
        except (ValueError, TypeError):
            cart[food_id_str] = 1
    else:
        cart[food_id_str] = 1

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{food.name} added to cart! 🛒❤️"
    )

    return redirect("cart")




# =========================================================
# CART
# =========================================================
@login_required
def cart(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    foods = []
    total = Decimal("0.00")


    for food_id, quantity in cart_data.items():

        try:

            quantity = int(quantity)

            if quantity < 1:
                quantity = 1

        except (
            ValueError,
            TypeError
        ):

            quantity = 1


        food = get_object_or_404(
            Food,
            id=food_id,
            available=True
        )


        item_total = (
            food.price * quantity
        )

        total += item_total


        foods.append(
            {
                "food": food,
                "quantity": quantity,
                "item_total": item_total,
            }
        )


    return render(
        request,
        "cart.html",
        {
            "foods": foods,
            "total": total,
        }
    )


# =========================================================
# INCREASE QUANTITY
# =========================================================

def increase_quantity(
    request,
    food_id
):

    food_id = str(food_id)

    cart = request.session.get(
        "cart",
        {}
    )


    if food_id in cart:

        try:

            cart[food_id] = (
                int(cart[food_id]) + 1
            )

        except (
            ValueError,
            TypeError
        ):

            cart[food_id] = 1


    request.session["cart"] = cart
    request.session.modified = True


    return redirect("cart")


# =========================================================
# DECREASE QUANTITY
# =========================================================

def decrease_quantity(
    request,
    food_id
):

    food_id = str(food_id)

    cart = request.session.get(
        "cart",
        {}
    )


    if food_id in cart:

        try:

            cart[food_id] = (
                int(cart[food_id]) - 1
            )

        except (
            ValueError,
            TypeError
        ):

            cart[food_id] = 0


        if cart[food_id] <= 0:

            del cart[food_id]


    request.session["cart"] = cart
    request.session.modified = True


    return redirect("cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(
    request,
    food_id
):

    food_id = str(food_id)

    cart = request.session.get(
        "cart",
        {}
    )


    if food_id in cart:

        del cart[food_id]


    request.session["cart"] = cart
    request.session.modified = True


    return redirect("cart")


# =========================================================
# CHECKOUT
# =========================================================

def checkout(request):

    cart_data = request.session.get(
        "cart",
        {}
    )


    if not cart_data:

        messages.warning(
            request,
            "Your cart is empty. 🍽️"
        )

        return redirect("cart")


    foods = []
    total = Decimal("0.00")


    for food_id, quantity in cart_data.items():

        try:

            quantity = int(quantity)

            if quantity < 1:
                quantity = 1

        except (
            ValueError,
            TypeError
        ):

            quantity = 1


        food = get_object_or_404(
            Food,
            id=food_id,
            available=True
        )


        item_total = (
            food.price * quantity
        )

        total += item_total


        foods.append(
            {
                "food": food,
                "quantity": quantity,
                "item_total": item_total,
            }
        )


    return render(
        request,
        "checkout.html",
        {
            "foods": foods,
            "total": total,
        }
    )





# =========================================================
# PLACE ORDER
# =========================================================

@login_required
def place_order(request):

    if request.method != "POST":

        return redirect(
            "checkout"
        )


    cart_data = request.session.get(
        "cart",
        {}
    )


    if not cart_data:

        messages.warning(
            request,
            "Your cart is empty. 🍽️"
        )

        return redirect(
            "cart"
        )
    
    #success_url = host + '/payment/success/?session_id={CHECKOUT_SESSION_ID}',
    

    # -----------------------------------------------------
    # CUSTOMER DETAILS
    # -----------------------------------------------------

    customer_name = request.POST.get(
        "customer_name",
        ""
    ).strip()

    phone = request.POST.get(
        "phone",
        ""
    ).strip()

    address = request.POST.get(
        "address",
        ""
    ).strip()

    payment_method = request.POST.get(
        "payment_method",
        ""
    ).strip()


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not customer_name:

        messages.error(
            request,
            "Please enter your name. ❤️"
        )

        return redirect(
            "checkout"
        )


    if not phone:

        messages.error(
            request,
            "Please enter your phone number. 📞"
        )

        return redirect(
            "checkout"
        )


    if not phone.isdigit():

        messages.error(
            request,
            "Please enter a valid phone number."
        )

        return redirect(
            "checkout"
        )


    if len(phone) < 10 or len(phone) > 15:

        messages.error(
            request,
            "Phone number must contain 10 to 15 digits."
        )

        return redirect(
            "checkout"
        )


    if not address:

        messages.error(
            request,
            "Please enter your delivery address. 📍"
        )

        return redirect(
            "checkout"
        )


    if not payment_method:

        messages.error(
            request,
            "Please select a payment method. 💳"
        )

        return redirect(
            "checkout"
        )


    valid_payment_methods = [
        choice[0]
        for choice in Order.PAYMENT_CHOICES
    ]


    if payment_method not in valid_payment_methods:

        messages.error(
            request,
            "Please select a valid payment method."
        )

        return redirect(
            "checkout"
        )


    # -----------------------------------------------------
    # CALCULATE TOTAL
    # -----------------------------------------------------

    total = Decimal("0.00")

    order_items = []


    for food_id, quantity in cart_data.items():

        try:

            quantity = int(quantity)

            if quantity < 1:
                quantity = 1

        except (
            ValueError,
            TypeError
        ):

            quantity = 1


        food = get_object_or_404(
            Food,
            id=food_id,
            available=True
        )


        item_total = (
            food.price * quantity
        )

        total += item_total


        order_items.append(
            {
                "food": food,
                "quantity": quantity,
            }
        )


    # -----------------------------------------------------
    # CREATE ORDER
    # -----------------------------------------------------

    order = Order.objects.create(

        user=request.user,

        customer_name=customer_name,

        phone=phone,

        address=address,

        payment_method=payment_method,

        total_amount=total,

        status="Order Placed",
    )


    # -----------------------------------------------------
    # CREATE ORDER ITEMS
    # -----------------------------------------------------

    for item in order_items:

        OrderItem.objects.create(

            order=order,

            food=item["food"],

            quantity=item["quantity"],

            price=item["food"].price,
        )


    # -----------------------------------------------------
    # CLEAR CART
    # -----------------------------------------------------

    request.session["cart"] = {}

  
   # -----------------------------------------------------
    # PAYMENT ROUTING
    # -----------------------------------------------------
   # -----------------------------------------------------
    # PAYMENT ROUTING (Simple & Working Card-Only)
    # -----------------------------------------------------
    if payment_method == "ONLINE":
        stripe.api_key = settings.STRIPE_SECRET_KEY
        host = request.build_absolute_uri('/')[:-1]

        stripe_amount = int(total * 100)
        if stripe_amount < 5000:
            stripe_amount = 5000

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            billing_address_collection='required',
            customer_email=request.user.email if request.user.is_authenticated and request.user.email else None,
            metadata={
                'order_id': order.id,
            },
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': stripe_amount,
                        'product_data': {
                            'name': f'Food Order #{order.id}',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=host + '/payment/success/?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=host + '/payment/cancel/',
        )
        return redirect(checkout_session.url, code=303)

    # COD fallback
    request.session["cart"] = {}
    messages.success(request, "Your order has been placed successfully! 🍴")
    return redirect("payment_success")

    # -----------------------------------------------------
    # payment  SUCCESS 
    # -----------------------------------------------------

import stripe
from django.conf import settings
from django.shortcuts import render
from .models import Order  # ensure Order model imported ho

def payment_success(request):
    session_id = request.GET.get('session_id')
    order = None

    if session_id:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Stripe se payment status fetch karein
            session = stripe.checkout.Session.retrieve(session_id, expand=['line_items'])
            if session.payment_status == 'paid':
                # Order ID description/line_items se nikalna ya session ke metadata se
                # Agar order status update karna hai:
                order_id = session.metadata.get('order_id')
                if order_id:
                    order = Order.objects.filter(id=order_id).first()
                    # Agar order mil gaya, toh status update bhi kar sakte hain
                    if order and order.status == "Order Placed":
                        order.status = "Paid / Processing"
                        order.save()
        except Exception as e:
            print("Stripe session error:", e)

    return render(request, 'payment_success.html', {'order': order})

# =========================================================
# ORDER SUCCESS
# =========================================================

@login_required
def order_success(
    request,
    order_id
):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )


    return render(
        request,
        "order_success.html",
        {
            "order": order
        }
    )


# =========================================================
# MY ORDERS
# =========================================================

@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items__food"
    ).order_by(
        "-order_date"
    )

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders
        }
    )





# =========================================================
# CANCEL ORDER
# =========================================================

@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if order.status == "Order Placed":

        order.status = "Cancelled"
        order.save(update_fields=["status"])

        messages.success(
            request,
            f"Order #{order.id} has been cancelled successfully."
        )

    else:

        messages.error(
            request,
            "This order cannot be cancelled now."
        )

    return redirect("my_orders")




# =========================================================
# CONTACT
# =========================================================

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()

        # NAME
        if not name:
            messages.error(
                request,
                "Please enter your name."
            )
            return redirect("contact")

        if len(name) < 2:
            messages.error(
                request,
                "Please enter a valid name."
            )
            return redirect("contact")

        # EMAIL
        if not email:
            messages.error(
                request,
                "Please enter your email address."
            )
            return redirect("contact")

        try:
            validate_email(email)

        except ValidationError:
            messages.error(
                request,
                "Please enter a valid email address."
            )
            return redirect("contact")

        # SUBJECT
        if not subject:
            messages.error(
                request,
                "Please enter a subject."
            )
            return redirect("contact")

        # MESSAGE
        if not message_text:
            messages.error(
                request,
                "Please enter your message."
            )
            return redirect("contact")

        if len(message_text) < 5:
            messages.error(
                request,
                "Please enter a meaningful message."
            )
            return redirect("contact")

        # SAVE MESSAGE IN DATABASE
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )

        messages.success(
            request,
            "Thank you for contacting Foodie! ❤️"
        )

        return redirect("contact")

    return render(
        request,
        "contact.html"
    )
   


   


# =========================================================
# REGISTER
# =========================================================

def register(request):

    if request.user.is_authenticated:

        return redirect(
            "home"
        )


    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )


        if not username:

            messages.error(
                request,
                "Please enter a username."
            )

            return render(
                request,
                "register.html"
            )


        if not email:

            messages.error(
                request,
                "Please enter your email."
            )

            return render(
                request,
                "register.html"
            )


        if not password:

            messages.error(
                request,
                "Please enter a password."
            )

            return render(
                request,
                "register.html"
            )


        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "register.html"
            )


        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return render(
                request,
                "register.html"
            )


        user = User.objects.create_user(

            username=username,

            email=email,

            password=password,
        )


        login(
            request,
            user
        )


        messages.success(
            request,
            "Account created successfully! Welcome to Foodie! ❤️"
        )


        return redirect(
            "home"
        )


    return render(
        request,
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:

        return redirect(
            "home"
        )


    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )


        if not username:

            messages.error(
                request,
                "Please enter your username."
            )

            return render(
                request,
                "login.html"
            )


        if not password:

            messages.error(
                request,
                "Please enter your password."
            )

            return render(
                request,
                "login.html"
            )


        user = authenticate(

            request,

            username=username,

            password=password,
        )


        if user is not None:

            login(
                request,
                user
            )


            messages.success(
                request,
                "Welcome back! ❤️"
            )


            next_url = request.GET.get(
                "next"
            )


            if next_url:

                return redirect(
                    next_url
                )


            return redirect(
                "home"
            )


        messages.error(
            request,
            "Invalid username or password."
        )


    return render(
        request,
        "login.html"
    )



# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):

    logout(
        request
    )


    messages.success(
        request,
        "You have been logged out. See you again! ❤️"
    )


    return redirect(
        "home"
    )



# =========================================================
# ADMIN DASHBOARD
# =========================================================

def admin_check(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(admin_check, login_url="login")
def admin_dashboard(request):

    total_foods = Food.objects.count()

    available_foods = Food.objects.filter(
        available=True
    ).count()

    unavailable_foods = Food.objects.filter(
        available=False
    ).count()

    total_orders = Order.objects.count()

    placed_orders = Order.objects.filter(
        status="Order Placed"
    ).count()

    preparing_orders = Order.objects.filter(
        status="Preparing"
    ).count()

    delivery_orders = Order.objects.filter(
        status="Out for Delivery"
    ).count()

    delivered_orders = Order.objects.filter(
        status="Delivered"
    ).count()

    cancelled_orders = Order.objects.filter(
        status="Cancelled"
    ).count()

    revenue = Order.objects.filter(
        status="Delivered"
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    recent_orders = Order.objects.all().order_by(
        "-order_date"
    )[:10]

    total_messages = ContactMessage.objects.count()

    unread_messages = ContactMessage.objects.filter(
        is_read=False
    ).count()

    context = {
        "total_foods": total_foods,
        "available_foods": available_foods,
        "unavailable_foods": unavailable_foods,

        "total_orders": total_orders,
        "placed_orders": placed_orders,
        "preparing_orders": preparing_orders,
        "delivery_orders": delivery_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,

        "revenue": revenue,

        "recent_orders": recent_orders,

        "total_messages": total_messages,
        "unread_messages": unread_messages,
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )


def create_checkout_session(request):
    # Live domain ke hisaab se redirect URLs set karein
    # Local par chalana ho toh 'http://127.0.0.1:8000' use karein
    # Live Render par chalana ho toh domain URL
    host = request.build_absolute_uri('/')[:-1]

    # Dummy product ya cart total amount (e.g., ₹500 = 50000 in smallest currency unit, or in USD 500 = 500 cents)
    # Stripe default USD/INR handle karta hai
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',  # Sandbox account US ka hai toh USD best rahega
                    'unit_amount': 2000,  # $20.00 (Cent mein count hota hai)
                    'product_data': {
                        'name': 'Foodie App Order',
                    },
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=host + '/payment/success/',
        cancel_url=host + '/payment/cancel/',
    )
    return redirect(checkout_session.url, code=303)


def payment_success(request):
    return render(request, 'payment_success.html')


def payment_cancel(request):
    return render(request, 'payment_cancel.html')