from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import Login
from django.core.paginator import Paginator, EmptyPage
from .models import Products
from .serializers import ProductsSerializer
from django.core.mail import send_mail
import os

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = Login.objects.get(username=username)
            if user is not None:
                if user.password == password:
                      refresh = RefreshToken.for_user(user)

                      custom_payload = {
                       'user_id': user.id,
                       'username': user.username,
                      }

                      refresh.payload.update(custom_payload)

                      access_token = str(refresh.access_token)
                      response = Response(access_token)
                      return response
            else:
              return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



        except Login.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ProductsAPIView(APIView):
    def get(self, request):
        unique_categories = Products.objects.values_list('product_category', flat=True).distinct()
        page_n = int(request.GET.get('page', 1))
        each_category_size = int(request.GET.get('page_size', 5))

        paginated_data = []
        next_page_numbers = {}
        previous_page_numbers = {}

        has_next = False  # Initialize has_next to False outside the loop

        for category in unique_categories:
            products = Products.objects.filter(product_category=category).order_by('product_id')
            p = Paginator(products, each_category_size)

            try:
                page = p.page(page_n)
            except EmptyPage:
                page = p.page(1)

            serializer = ProductsSerializer(page, many=True)
            paginated_data.extend(serializer.data)
            next_page_numbers[category] = page.next_page_number() if page.has_next() else None
            previous_page_numbers[category] = page.previous_page_number() if page.has_previous() else None


            has_next = has_next or page.has_next()

        # Return serialized data with pagination information for each category
        return Response({
            'results': paginated_data,
            'next': next_page_numbers,
            'previous': previous_page_numbers,
            'has_next': has_next,
        })

    def post(self, request):
        
     try:
        product_serializer = ProductsSerializer(data=request.data)
        if product_serializer.is_valid():
            product_instance = product_serializer.save()  
            serialized_product_data = product_serializer.data
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

     return Response(serialized_product_data, status=status.HTTP_201_CREATED)

    def delete(self, request, product_id):
        try:
            to_delete_product = Products.objects.get(product_id=product_id)
            if to_delete_product is not None:
                image_path = to_delete_product.product_image.path
                to_delete_product.delete()
                if os.path.exists(image_path):
                    os.remove(image_path)
                return Response(f'{product_id} product id deleted successfully')
        except Products.DoesNotExist:
            return Response(f'Product with ID {product_id} does not exist', status=status.HTTP_404_NOT_FOUND)

class MailAPI(APIView):
        def post(self, request):
         print(request.data)
         name = request.data.get('name')
         email = request.data.get('email')
         phone = request.data.get('phone')
         message = request.data.get('message')

         email_subject = 'Contact Form Submission'
         email_message = f"Name: {name}\nPhone: {phone}\nEmail: {email}\nMessage: {message}"

         send_mail(
                email_subject,
                email_message,
                'spandanbhattarai79@gmail.com',  
                ['spandanbhattarai79@gmail.com'],  
                fail_silently=False,
                auth_user='spandanbhattarai79@gmail.com',  
                auth_password='vwcp cuvj pjss qzdg',  
            )
         return Response({'success': True})
        
class GetAPIView(APIView):
    def get(self, request):
        product = Products.objects.all()
        serializer = ProductsSerializer(product, many=True)
        return Response(serializer.data)