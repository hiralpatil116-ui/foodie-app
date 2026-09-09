from django.db import models
from django.contrib.auth.models import User


class Food(models.Model):

    CATEGORY_CHOICES = [
        ("Pizza", "Pizza"),
        ("Burger", "Burger"),
        ("Indian", "Indian Food"),
        ("Chinese", "Chinese Food"),
        ("Pasta", "Pasta"),
        ("Dessert", "Dessert"),
        ("Drinks", "Drinks"),
        ("Jain", "Jain Food"),
    ]

    name = models.CharField(max_length=200)

    category = models.CharField(
        max_length=255,
        choices=CATEGORY_CHOICES
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    image = models.ImageField(
        upload_to="food_images/",
        max_length=500,
        blank=True,
        null=True
    )

    available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.name


class Order(models.Model):

    PAYMENT_CHOICES = [
    ('COD', 'Cash on Delivery'),
    ('ONLINE', 'Online Payment'),
]

    STATUS_CHOICES = [
        ("Order Placed", "Order Placed"),
        ("Preparing", "Preparing"),
        ("Out for Delivery", "Out for Delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    order_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Order Placed"
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.food.name} x {self.quantity}"


class ContactMessage(models.Model):

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.name} - {self.subject}"