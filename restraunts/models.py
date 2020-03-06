from django.db import models
from django.utils import timezone
# Create your models here.

class Restraunt(models.Model):
    name            = models.CharField(max_length = 36)
    city            = models.CharField(max_length = 16)
    address         = models.CharField(max_length = 36)
    state           = models.CharField(max_length = 16)
    seatsAvailable  = models.IntegerField()
    cuisine         = models.CharField(max_length = 16)
    beginTime       = models.TimeField()
    endTime         = models.TimeField()
    priceRange      = models.CharField(max_length = 16)
    
   
DEFAULT_ID = 1

class ReservationDate(models.Model): 
    restraunt       = models.ForeignKey(Restraunt, on_delete = models.CASCADE, default = DEFAULT_ID)
    date            = models.DateField(default = timezone.now)

class TodayReservation(models.Model):
    # Don't need this but not enough time to change
    reservationDate     = models.ForeignKey(ReservationDate, on_delete = models.CASCADE, default = DEFAULT_ID)
 

class ReservationInterval(models.Model):
    day                     = models.ForeignKey(TodayReservation, on_delete = models.CASCADE, default = DEFAULT_ID)
    timeIntervalBegin       = models.IntegerField()
    timeIntervalEnd         = models.IntegerField()
    seatsLeft               = models.IntegerField()

class Seat(models.Model):
    timeInterval        = models.ForeignKey(ReservationInterval, on_delete = models.CASCADE, default = DEFAULT_ID)
    