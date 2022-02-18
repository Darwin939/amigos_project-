from django.contrib.auth.models import User
from django.db import models

ORDER_STATUS_CHOICES = (
    ('OrderEvent', 'OrderEvent'),
    ('OrderCancelEvent', 'OrderCancelEvent'),
    ('OrderFreightReceiveEvent', 'OrderFreightReceiveEvent'),
    ('OrderFulfillmentEvent', 'OrderFulfillmentEvent'),
    ('OrderFailEvent', 'OrderFailEvent'),
)

OFFER_CHOICES = (
    ('OfferEvent', 'OfferEvent'),
    ('OfferAcceptEvent', 'OfferAcceptEvent'),
)


class Location(models.Model):
    location_id = models.IntegerField()
    name = models.CharField(max_length=255)
    coordinateX = models.FloatField()
    coordinateY = models.FloatField()
    srid = models.CharField(max_length=255)

class Delivery_Company(models.Model):
    delivery_company_id = models.IntegerField()
    name = models.CharField(max_length=255)
    date = models.DateTimeField()

class Order(models.Model):

    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    weightKG = models.FloatField(null=True, blank=True)
    expectingPriceTenge = models.FloatField(null=True, blank=True)
    expectingDeliveryDate = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True, auto_now=True)
    FromLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='from_location_order', null=True, blank=True)
    ToLocation = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='to_location_order', null=True, blank=True)
    type = models.CharField(max_length=255, choices=ORDER_STATUS_CHOICES, null=True, blank=True)
    fail_reason = models.IntegerField(null=True, blank=True)
    cancel_reason = models.IntegerField(null=True, blank=True)

class Offer(models.Model):

    delivery_Company = models.ForeignKey(Delivery_Company, on_delete=models.CASCADE)
    offeredPriceTenge = models.FloatField()
    date = models.DateTimeField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='offers')
    type = models.CharField(max_length=255, choices=OFFER_CHOICES)

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('buyer', 'buyer'),
        ('logist' , 'logist'),
    )

    user_type = models.CharField(max_length=255, choices=USER_TYPE_CHOICES)
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE, blank=True, null=True)
