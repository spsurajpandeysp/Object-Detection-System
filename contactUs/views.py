from django.shortcuts import render
from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from contactUs.models import ContactUs
# Create your views here.
def contactUs(request):
    data= {
        'url':'contactUs',
    }
    try:
        if request.method=="POST":
            name = request.POST['name']
            email = request.POST['email']
            message = request.POST['message']
            html_content  = render_to_string('contactUsMail.html',{'fullName':name,'emailId':email,'message':message})
            text_content = strip_tags(html_content)
            en = ContactUs(fullName=name,emailId=email,message=message)
            en.save()
            mail = EmailMultiAlternatives(
                "Your Request Sucessfully Submitted",
                text_content,
                'objectdetectionsystem@gmail.com',
                [email],
            )
            mail.attach_alternative(html_content,'text/html')
            result = mail.send()
            if result > 0:
                return render(request,'thankyou.html',data)
            else:
                print("Email failed to send")
    except Exception as e:
        print(e)
    return render(request,'contactUs.html')