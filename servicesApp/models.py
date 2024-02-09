from django.db import models

# Create your models here.
class ServicesModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    title = models.CharField(max_length=100,null=True,blank=False)
    file = models.FileField(null=True,default=None,max_length=250,upload_to='servicesImage/')
    paragraph=models.TextField(max_length=10000,null=True,blank=False)
