from django import forms
from admin_analytics_service.models import Location

class ClientForm(forms.Form):
    Name = forms.CharField(label='Name', max_length=40)
    weightKG = forms.FloatField(label='Weight' , required=False)
    expectingPriceTenge = forms.FloatField(label='PriceTenge', required=False)
    expectingDeliveryDate = forms.DateTimeField(label='DeliveryDate', required=False)
    FromLocation = forms.MultipleChoiceField(choices=Location.objects.values_list('name'), label="FromLocation")
    ToLocation = forms.MultipleChoiceField(choices=Location.objects.values_list('name'), label="ToLocation")
