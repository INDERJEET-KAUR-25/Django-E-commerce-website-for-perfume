from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    # Ensure this field name matches what you use in views.py
    image = models.ImageField(upload_to='products/', null=True, blank=True) 
    stock = models.IntegerField(default=10)

    def __str__(self):
        return self.name