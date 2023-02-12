from .models import EmailHistribution
from django.forms import ModelForm, EmailInput

class HistributionForm(ModelForm):
    class Meta:
        model = EmailHistribution
        fields = ['email']

        widgets = {
            'email': EmailInput(attrs={
                "placeholder": "historylover@mail.com",
                'type': 'email'
            })
        }