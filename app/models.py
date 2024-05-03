
# Create your models here.
from django.db import models

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_image = models.ImageField(upload_to='images/')
    product_description = models.CharField(max_length=1000)
    product_category = models.CharField(max_length = 30)

class Login(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

