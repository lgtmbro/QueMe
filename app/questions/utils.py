import os
import random
import datetime
import pytz
from twilio.rest import Client
from PIL import ImageDraw, Image, ImageFont

account_sid = os.environ.get("TWILIO_SID")
auth_token = os.environ.get("TWILIO_TOKEN")
twilio_number = os.environ.get("TWILIO_WA_NUMBER")

success_gifs = [
    "https://static.designboom.com/wp-content/uploads/2013/03/thumbsAmmo021.jpg",
    "https://static.designboom.com/wp-content/uploads/2013/03/thumbsAmmo03.jpg",
    "https://media.wired.com/photos/5933668e7965e75f5f3c7bca/master/pass/biglebowskytumb.jpg",
    "https://i.pinimg.com/originals/e0/0a/5d/e00a5d51ffa516ef2b64ea1ff3a3a60a.jpg",
    "https://www.memesmonkey.com/images/memesmonkey/42/42410cc23c68750b4f3e7f50e89505ab.jpeg",
]

def whatsapp_reply(msisdn, message, media_urls=None):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to=f"whatsapp:{msisdn}",
        from_=f"whatsapp:{twilio_number}",
        body=message,
        media_url=media_urls,
    )
    return message


def random_success_gif():
    return success_gifs[random.randint(0, len(success_gifs) - 1)]

def create_certificate(name="You"):
    date = datetime.datetime.now().strftime("%d-%m-%Y")

    filename = name.replace(" ", "_").lower()

    img = Image.open("questions/static/certificate.png")
    img_width = img.width

    draw = ImageDraw.Draw(img)

    name_font = ImageFont.truetype("questions/static/fnt.ttf", 80)
    name_text_width, name_text_height = draw.textsize(name, font=name_font)

    date_font = ImageFont.truetype("questions/static/fnt.ttf", 60)
    date_text_width, name_text_height = draw.textsize(date, font=date_font)
    
    draw.text(((img_width-name_text_width)/2, 730), name, (175,85,0), font=name_font)
    draw.text(((img_width-date_text_width)/2, 1050), date, (175,85,0), font=date_font)

    img.save(f'questions/static/public/{filename}.png')

    return f'{filename}.png'