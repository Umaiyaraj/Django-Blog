from django import forms
from .models import Contact
import re

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

   
    
    def clean_name(self):
        name = self.cleaned_data['name']

        if not re.match(r'^[A-Za-z ]+$', name):
            raise forms.ValidationError(
                "Name should contain only letters and spaces."
            )

        return name


