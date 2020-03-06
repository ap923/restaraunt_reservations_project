from django import forms

from .models import Restraunt

class RestrauntModelForm(forms.ModelForm):
    class Meta:
        model = Restraunt
        fields = [
            'name',
            'city',
            'address',
            'state',
            'seatsAvailable',
            'cuisine',
            'beginTime',
            'endTime',
            'priceRange'
            
        ]
    #def clean_name(self):
    #    self = self.cleaned_data.get('name')
    #    if name.lower() == 'abc':
    #        raise forms.ValidationError("This is not a valid name")
    #    return name