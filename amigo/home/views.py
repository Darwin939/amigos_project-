

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Sum


from django.apps import apps

@login_required(login_url="/login/")
def index(request):
    Order =  apps.get_model(app_label='admin_analytics_service', model_name='Order')
    context = {'segment': 'index',
               'order_count': Order.objects.all().count,
               'order_this_month_count': Order.objects.filter(date__range=["2022-01-01", "2022-02-28"]).count,
               'turn_over_this_month':Order.objects.filter(date__range=["2022-01-01", "2022-02-28"]).aggregate(Sum('expectingPriceTenge'))['expectingPriceTenge__sum'],
               'turn_over': Order.objects.all().aggregate(Sum('expectingPriceTenge'))['expectingPriceTenge__sum'],
               'order_list':Order.objects.all(),
               }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
