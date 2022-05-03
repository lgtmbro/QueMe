import os
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_TOKEN")
twilio_number = os.environ.get('TWILIO_WA_NUMBER')

client = Client(account_sid, auth_token)

def whatsapp_reply(msisdn, message, media_url=None):
    message = client.messages.create(
        to=f'whatsapp:{msisdn}',
        from_=f'whatsapp:{twilio_number}',
        body=message,
        media_url=media_url
    )
    return message
