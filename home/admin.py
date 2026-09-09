from django.contrib import admin
from .models import Food, Order, OrderItem, ContactMessage


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available")
    list_filter = ("category", "available")
    search_fields = ("name", "description")
    list_editable = ("available",)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("food", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "phone",
        "payment_method",
        "total_amount",
        "status",
        "order_date",
    )

    list_editable = (
    "status",
)

    list_filter = ("payment_method", "status", "order_date")
    search_fields = ("customer_name", "phone", "address" ,"user__username",)

    inlines = [OrderItemInline]

    readonly_fields = (
        "customer_name",
        "phone",
        "address",
        "payment_method",
        "total_amount",
        "order_date",
        "user",
    )


   


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "subject",
        "created_at",
        "is_read",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "subject",
        "message",
    )

    readonly_fields = (
        "name",
        "email",
        "subject",
        "message",
        "created_at",
    )