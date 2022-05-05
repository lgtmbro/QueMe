
from os import environ
from django.core.management.base import BaseCommand
from questions.utils import create_certificate, whatsapp_reply
from questions.models import Customer

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for customer in Customer.objects.filter(msisdn="+27657118765"):
            if not customer.has_certificate:
                cert = create_certificate(customer.profile_name)
                if int(environ.get("DEBUG", 0)) == 0:
                    file_path = f'http://{environ.get("HOSTED_URL")}/static/{cert}'
                else:
                    file_path = f'http://localhost:8000/static/{cert}'
                message = """✨ A huge thank you for trying out this little whatsapp bot,\n\nit was extremely fun to put together. However the time has come to put this bot to rest.\n\n🎆Please print out and hang this certificate on you wall! 🤣"""
                whatsapp_reply(customer.msisdn, message, [file_path])
                print(cert)
