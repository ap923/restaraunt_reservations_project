from django import forms

from .models import Reservation

class ReservationModelForm(forms.ModelForm):
   

    class Meta:
        model = Reservation
        fields = [
            'first_name',
            'last_name',
            'phone',
            'email',
            'time_of_reservation',
            'reservation_comments',
            'restraunt_reserved',
            
        ]
        widgets = {
            'restraunt_reserved' : forms.HiddenInput(), 
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'reservation_comments': forms.TextInput(attrs={'placeholder': 'Reservation comments'}),
            'time_of_reservation' : forms.TextInput(attrs={'placeholder': 'hh:mm format'}),
        
        }
      