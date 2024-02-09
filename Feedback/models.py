from django.db import models

# Create your models here.
class Feedback(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    firstName = models.CharField(max_length=50,blank=False,null=False)
    lastName = models.CharField(max_length=50,blank=False,null=False)
    emailId = models.EmailField(max_length=100,blank=False,null=False)
    gender = models.CharField(max_length=10,blank=False,null=False)
    comp = models.TextField(max_length=10000,blank=False,null=False)
    rating = models.IntegerField(default=0,null=False,blank=False)