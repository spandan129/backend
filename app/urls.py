from django.urls import path
from .views import LoginView
from .views import ProductsAPIView, GetAPIView
from django.conf import settings
from django.conf.urls.static import static
from .views import MailAPI

urlpatterns = [
    path('login', LoginView.as_view(), name='login'),
    path('products', ProductsAPIView.as_view(), name='products-api'),
    path('product', GetAPIView.as_view(), name='getproduct'),
    path('products/<str:product_id>', ProductsAPIView.as_view(), name='products-api-detail'),
    path('sendemail', MailAPI.as_view(), name='send_email'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)