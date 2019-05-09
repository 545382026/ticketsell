from django.contrib import admin
from .models import Users, Tickets, BuyTicket
# Register your models here.

admin.site.register(Users)
admin.site.register(Tickets)
admin.site.register(BuyTicket)
