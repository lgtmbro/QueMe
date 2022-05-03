from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, HttpResponse

from .models import Customer


# Create your views here.

@csrf_exempt
def twilio_messages_ingress(request):
    if request.method != "POST":
        raise HttpResponseBadRequest("Invalid Request.")
    msisdn = f"+{request.POST.get('WaId')}"
    profile_name = request.POST.get('ProfileName')

    try:
        customer = Customer.objects.get(msisdn=msisdn)
    except:
        customer = False

    if not customer:
        customer = Customer.objects.create(msisdn=msisdn, profile_name=profile_name)

    print(customer)

    return HttpResponse("OK")