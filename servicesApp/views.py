from django.shortcuts import render
from .models import ServicesModel
# Create your views here.
def services(request):
    msqlData = ServicesModel.objects.only('title','paragraph','file')
    data = {
        'servicesData':msqlData
    }
    return render(request,'services.html',data)
