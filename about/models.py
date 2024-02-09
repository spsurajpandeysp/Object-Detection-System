from django.db import models

# Create your models here.
class About(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    title = models.CharField(max_length=100,null=False,blank=False)
    paragraph=models.TextField(max_length=10000,null=False,blank=False)