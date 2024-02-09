from django.db import models
class ContactUs(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    fullName = models.CharField(max_length=50,null=False,blank=False)
    emailId =  models.EmailField(max_length=100,null=False,blank=False)
    message = models.TextField(max_length=10000,null=False,blank=False)


# Create your models here.
