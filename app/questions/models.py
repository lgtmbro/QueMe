from django.db import models

# Create your models here.

class Customers(models.Model):
    msisdn = models.TextField()
    profile_name = models.TextField()


class Questions(models.Model):
    content = models.TextField()
    active = models.BooleanField(default=False)


class Asks(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    answer = models.TextField()
    status = models.TextField()
