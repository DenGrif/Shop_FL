# shop/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order
from django.forms.widgets import DateInput, TimeInput


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_date', 'delivery_time', 'delivery_address', 'comment']
        widgets = {
            'delivery_date': DateInput(attrs={'type': 'date'}),
            'delivery_time': TimeInput(attrs={'type': 'time'}),
        }
