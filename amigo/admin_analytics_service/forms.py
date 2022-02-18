from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.
from django.forms import ModelForm, widgets
from django.shortcuts import render, redirect

from .models import Order


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        # user.
        if commit:
            user.save()
        return user


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderCreateForm(ModelForm):
    expectingDeliveryDate = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = ('weightKG', 'expectingDeliveryDate',
                  'FromLocation', 'ToLocation')
        widgets = {
            'expectingDeliveryDate': forms.DateInput,
        }

    def save(self, user=None,  commit=True, *args, **kwargs):
        order = super().save(commit=False, *args, **kwargs)
        order.type = 'OrderEvent'

        # self.request = kwargs.pop("request")
        c = self.get_context()

        order.client = self.request.user
        if commit:
            order.save()
        return order
