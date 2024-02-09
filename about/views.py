from django.shortcuts import render
from about.models import About
# Create your views here.
def aboutUs(request):
    sqlData = About.objects.only('title','paragraph')
    data = {
        'aboutUsData':sqlData
    }
    return render(request,'about.html',data)