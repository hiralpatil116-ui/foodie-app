from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from home import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),

    path(
        'create-checkout-session/',
        views.create_checkout_session,
        name='create_checkout_session',
    ),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
]



if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


    