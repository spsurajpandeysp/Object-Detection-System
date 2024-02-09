from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from Feedback.models import Feedback
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.

def feedback(request):
    data ={
        'url':'feedback'
    }
    try:
        if(request.method=='POST'):
            firstName = request.POST['firstName']
            lastName = request.POST['lastName']
            email = request.POST['email']
            gender = request.POST['gender']
            rating = request.POST['rating']
            message = request.POST['message']
            en = Feedback(firstName=firstName,lastName=lastName,emailId=email,gender=gender,rating=int(rating),comp=message)
            en.save()
            html_content = render_to_string('feedbackMail.html',{'firstName':firstName,'lastName':lastName,'emailId':email,'gender':gender,'rating':rating,'message':message})
            text_content = strip_tags(html_content)
            mail = EmailMultiAlternatives(
                'Feedback Form Successfully Submited',
                text_content,
                'objectdetectionsystem@gmail.com',
                [email]
            )
            mail.attach_alternative(html_content,'text/html')
            mail.send()
            return render(request,'thankyou.html',data)
    except Exception as e:
        print(e)
    return render(request,'feedback.html')


