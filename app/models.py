from django.db import models

# Create your models here.
class Item(models.Model):
    productname = models.CharField(max_length=100)
    price = models.IntegerField(null= True, blank=True)

    def __str__(self):
        return self.productname
    