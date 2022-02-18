from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.
from django.forms import ModelForm, widgets
from django.shortcuts import render, redirect

from .models import Order, Offer, Delivery_Company, UserProfile


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)

        profile = UserProfile(user=user, user_type='buyer')
        if commit:
            user.save()
            profile.save()
        return user


class NewUserLogistForm(UserCreationForm):
    delivery_company_name = forms.CharField()

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)

        deliv_comp = Delivery_Company(name = self.cleaned_data['delivery_company_name'])
        deliv_comp.save()
        profile = UserProfile(delivery_company = deliv_comp, user=user, user_type='logist')

        if commit:
            user.save()
            profile.save()
        return user



class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = 'date'

class OfferCreateForm(ModelForm):
    user = forms.IntegerField(widget=forms.HiddenInput)
    order = forms.IntegerField(widget=forms.HiddenInput)


    class Meta:
        model = Offer
        fields = ('offeredPriceTenge',)



    def save(self, user=None, commit=True, *args, **kwargs):
        offer = super().save(commit=False, *args, **kwargs)
        offer.type = 'OfferEvent'
        delivery_company = User.objects.get(pk=int(self.cleaned_data['user'])).userprofile.delivery_company
        offer.delivery_Company = delivery_company
        offer.order = Order.objects.get(pk=self.cleaned_data['order'])



        if commit:
            offer.save()
        return offer



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
