from django.db import models
from django.urls import reverse

# Create your models here.



class Reservation(models.Model):
    first_name           = models.CharField(max_length=16)
    last_name            = models.CharField(max_length=16)
    email                = models.CharField(max_length=16)
    phone                = models.IntegerField()
    restraunt_reserved   = models.TextField(max_length = 24,blank = True, )
    time_when_reserved   = models.DateTimeField(auto_now_add = True) #useful for owner to see popular times people are reserving
    date_of_reservation  = models.DateField("2020-01-01")

    time_of_reservation  = models.TimeField()
    reservation_comments = models.CharField(max_length = 162, blank = True, null = True) #If customer has special requests

    def get_absolute_url(self):
        return reverse("reservations:reservation-detail", kwargs = {"id" : self.id})

    

    