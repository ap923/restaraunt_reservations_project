from django.contrib import admin

from .models import Restraunt, ReservationDate, TodayReservation , ReservationInterval, Seat #relative import because admin.py and models.py are on the same directory


# Register your models here.
admin.site.register(Restraunt)
admin.site.register(ReservationDate)
admin.site.register(ReservationInterval)
admin.site.register(TodayReservation)
admin.site.register(Seat)



