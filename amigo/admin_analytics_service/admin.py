from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Location)


admin.site.register(models.Delivery_Company)


admin.site.register(models.Order)

admin.site.register(models.Offer)

admin.site.register(models.UserProfile)