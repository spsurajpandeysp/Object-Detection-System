from django.db import models

# Create your models here.
class complainModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    firstName = models.CharField(max_length=50,blank=False,null=False)
    lastName = models.CharField(max_length=50,blank=False,null=False)
    email = models.EmailField(max_length=100,blank=False,null=False)
    image = models.FileField(max_length=250,null=True,default=False,upload_to='complainImage/')
    message = models.TextField(max_length=1000,blank=False,null=False)