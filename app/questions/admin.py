from django.contrib import admin
from .models import Customer, Question, Ask

# Register your models here.

admin.site.register(Customer)
admin.site.register(Question)
admin.site.register(Ask)
