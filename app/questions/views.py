from datetime import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.exceptions import BadRequest
from datetime import datetime, timezone

from .utils import whatsapp_reply, random_success_gif

from .models import Customer, Question, Ask


@csrf_exempt
def twilio_messages_ingress(request):
    if request.method != "POST":
        raise BadRequest("Invalid Request.")

    msisdn = f"+{request.POST.get('WaId')}"
    profile_name = request.POST.get("ProfileName")
    body = request.POST.get("Body")

    if None in [msisdn, profile_name]:
        raise BadRequest("Invalid Request.")

    try:
        customer = Customer.objects.get(msisdn=msisdn)
    except:
        customer = False

    if not customer:
        customer = Customer.objects.create(msisdn=msisdn, profile_name=profile_name)

    current_ask = (
        Ask.objects.filter(customer=customer).filter(answer__isnull=True).first()
    )

    if current_ask:
        delta = datetime.now(timezone.utc) - current_ask.created_at
        if (delta.seconds / 3600) > 12:
            current_ask.delete()

    if current_ask:
        current_ask.answer = body
        current_ask.status = "answered"
        current_ask.save()

        active_questions_count = (
            Question.objects.order_by("-created_at").filter(active=True).count()
        )
        answered_count = Ask.objects.filter(customer=customer).count()
        unanswered = active_questions_count - answered_count
        unanswered_reply = f"You have {unanswered} unanswered questions! Reply to us again to get another question!"
        no_more_questions_reply = (
            "You have answered all our questions! Check back soon for more! 🤘"
        )

        success_msg = f"\
*🥳 Done!*\n\n\
*Question:*\n{current_ask.question.content}?\n\n\
*Answer:*\n{current_ask.answer}\n\n\
👍 Great job {customer.profile_name}! \
{unanswered_reply if unanswered > 0 else no_more_questions_reply}"

        whatsapp_reply(msisdn, success_msg, [random_success_gif()])
    else:
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
                msisdn,
                "🎆 *You are all up to date!*\n\nWe currently dont have anymore questions for you, check back soon for more questions 🥳",
            )
        else:
            Ask.objects.create(customer=customer, question=selected_question)
            whatsapp_reply(msisdn, f"*🤔 Question*: {selected_question.content}?")

    return HttpResponse("OK")
