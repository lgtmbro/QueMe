from datetime import datetime, timezone
import time

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.exceptions import BadRequest

from .utils import whatsapp_reply, random_success_gif

from .models import Customer, Question, Ask

def ask_a_question(customer):
        answered_question_ids = [
            ask["question_id"]
            for ask in Ask.objects.filter(customer=customer).values("question_id")
        ]
        active_questions = Question.objects.order_by("-created_at").filter(active=True)

        selected_question = False
        for question in active_questions:
            if question.id not in answered_question_ids and selected_question is False:
                selected_question = question

        if selected_question is False:
            whatsapp_reply(
                customer.msisdn,
                "🎆 *You are all up to date!*\n\nWe currently dont have anymore questions for you, check back soon for more questions 🥳",
            )
        else:
            Ask.objects.create(customer=customer, question=selected_question)
            whatsapp_reply(customer.msisdn, f"*🤔 Question*: {selected_question.content}?")


@csrf_exempt
def twilio_messages_ingress(request):
    if request.method != "POST":
        raise BadRequest("Invalid Request.")

    msisdn = f"+{request.POST.get('WaId')}"
    profile_name = request.POST.get("ProfileName")
    body = request.POST.get("Body")

    if len(body) == 0:
        whatsapp_reply(msisdn, "Please reply with a message.")
        return HttpResponse("OK")

    if None in [msisdn, profile_name]:
        raise BadRequest("Invalid Request.")

    try:
        customer = Customer.objects.get(msisdn=msisdn)
    except:
        customer = False

    if not customer:
        customer = Customer.objects.create(msisdn=msisdn, profile_name=profile_name)

    current_ask = (
        Ask.objects.filter(customer=customer).filter(status="initialized").first()
    )

    if current_ask:
        delta = datetime.now(timezone.utc) - current_ask.created_at
        if (delta.total_seconds() / 3600) > 12:
            current_ask.delete()
            current_ask = None

    if current_ask:
        current_ask.answer = body
        current_ask.status = "answered"
        current_ask.save()

        active_questions_count = (
            Question.objects.order_by("-created_at").filter(active=True).count()
        )


        success_msg = f"\
*🥳 Done!*\n\n\
*Question:*\n{current_ask.question.content}?\n\n\
*Answer:*\n{current_ask.answer}\n\n\
👍 Great job {customer.profile_name}!"

        whatsapp_reply(msisdn, success_msg, [random_success_gif()])
        time.sleep(0.5) # twilios send_at function was not working, so I had to compromise :/
        ask_a_question(customer=customer)
    else:
        ask_a_question(customer)

    return HttpResponse("OK")
