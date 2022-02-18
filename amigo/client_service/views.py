from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from admin_analytics_service.models import Order
from admin_analytics_service.models import Location


from .forms import ClientForm

def get_client_form(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ClientForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            order = Order()
            order.weightKG = form.weightKG
            order.expectingPriceTenge = form.expectingPriceTenge
            order.expectingDeliveryDate = form.expectingDeliveryDate
            order.date = datetime.now()
            order.FromLocation = form.FromLocation
            order.ToLocation = form.ToLocation
            order.type = 'Hackathon2022.OrderEvent, Hackathon2022'
            order.save()

            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        l = Location()
        l.location_id = 12
        l.name = 'uter'
        l.coordinateX = 12.3
        l.coordinateY = 1231.56
        l.srid = '1243'
        l.save()
        form = ClientForm()

    return render(request, 'index_main.html', {'form': form})