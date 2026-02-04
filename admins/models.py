from django.db import models

# Create your models here.
class admins(models.Model):
    adminname=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)

    def __str__(self):
        return self.adminname
    
    
