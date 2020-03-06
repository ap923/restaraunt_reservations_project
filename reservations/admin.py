from django.contrib import admin

from .models import Reservation #relative import because admin.py and models.py are on the same directory


# Register your models here.
admin.site.register(Reservation)