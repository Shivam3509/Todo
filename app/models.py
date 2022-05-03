from django.db import models

# Create your models here.
class Item(models.Model):
    productname = models.CharField(max_length=100)
    price = models.IntegerField(null= True, blank=True)

    def __str__(self):
        return self.productname
    

class Record(models.Model):
    productname = models.ForeignKey(Item, on_delete = models.CASCADE, related_name="records")
    quantity = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True, blank=True)

    
    