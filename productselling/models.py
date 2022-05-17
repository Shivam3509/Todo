from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    avaliable = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=100)
    shopname = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)
    gst = models.IntegerField(null=True, blank=True)

class Notification(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='to_user')
    message = models.TextField(null=True, blank=True)
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)