from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.exceptions import BadRequest

from .utils import whatsapp_reply

from .models import Customer, Question


# Create your views here.

@csrf_exempt
def twilio_messages_ingress(request):
    if request.method != "POST":
        raise BadRequest("Invalid Request.")

    msisdn = f"+{request.POST.get('WaId')}"
    profile_name = request.POST.get('ProfileName')

    if None in [msisdn, profile_name]:
        raise BadRequest("Invalid Request.")

    try:
        customer = Customer.objects.get(msisdn=msisdn)
    except:
        customer = False

    if not customer:
        customer = Customer.objects.create(msisdn=msisdn, profile_name=profile_name)

    question = Question.objects.get(active=True)


    whatsapp_reply(msisdn, "*GOT IT*")

    return HttpResponse("OK")