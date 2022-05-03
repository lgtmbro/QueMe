import os
import random
from twilio.rest import Client

account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_TOKEN")
twilio_number = os.environ.get("TWILIO_WA_NUMBER")

client = Client(account_sid, auth_token)

success_gifs = [
    "https://static.designboom.com/wp-content/uploads/2013/03/thumbsAmmo021.jpg",
    "https://static.designboom.com/wp-content/uploads/2013/03/thumbsAmmo03.jpg",
    "https://media.wired.com/photos/5933668e7965e75f5f3c7bca/master/pass/biglebowskytumb.jpg",
    "https://i.pinimg.com/originals/e0/0a/5d/e00a5d51ffa516ef2b64ea1ff3a3a60a.jpg",
    "https://www.memesmonkey.com/images/memesmonkey/42/42410cc23c68750b4f3e7f50e89505ab.jpeg",
]


def whatsapp_reply(msisdn, message, media_urls=None):
    message = client.messages.create(
        to=f"whatsapp:{msisdn}",
        from_=f"whatsapp:{twilio_number}",
        body=message,
        media_url=media_urls,
    )
    return message


def random_success_gif():
    return success_gifs[random.randint(0, len(success_gifs) - 1)]
