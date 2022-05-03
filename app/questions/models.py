from django.db import models

# Create your models here.


class Customer(models.Model):
    msisdn = models.TextField()
    profile_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"C: {self.profile_name} @ {self.msisdn}"


class Question(models.Model):
    content = models.TextField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Q: {self.content}"


class Ask(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
    status = models.TextField(default="initialized")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
