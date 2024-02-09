from django.shortcuts import render
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from complainApp.models import complainModel
from django.template.loader import get_template
from django.utils.html import strip_tags
# Create your views here.
def complain(request):
    data = {
        'url':'complain'
    }
    try:
        if request.method=='POST':
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            image = request.FILES['image']
            message = request.POST['complain']
            print(fname ,lname,email,message)
            en =  complainModel(firstName=fname,lastName=lname,email=email,image=image,message=message)
            en.save()

            html_content = render_to_string('complainMail.html',{'firstName':fname,'lastName':lname,'image':image,'email':email,'message':message})
            text_content = strip_tags(html_content)
            mail = EmailMultiAlternatives(
                "Successfully Complain is Submitted",
                text_content,
                'objectdetectionsystem@gmail.com',
                [email],
            )
            mail.attach_alternative(html_content,'text/html')
            mail.send() 
            return render(request,'thankyou.html',data) 
    except:
        pass
    return render(request,'complain.html')