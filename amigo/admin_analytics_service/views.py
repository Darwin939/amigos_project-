from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import F
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django.shortcuts import  render, redirect
from django.views.generic import ListView, CreateView, DetailView

from .forms import NewUserForm, OrderForm, OrderCreateForm, OfferCreateForm, NewUserLogistForm
from django.contrib.auth import login
from django.contrib import messages

from .models import Order, Offer


def register_request(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="create_user.html", context={"register_form":form})


def register_logist_request(request):
	if request.user.is_authenticated:
		return redirect('/')


	if request.method == "POST":
		form = NewUserLogistForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserLogistForm()
	return render (request=request, template_name="create_user_logist.html", context={"register_form":form})


def index(request):
	return render (request=request, template_name="index_main.html")

class OrderListView(ListView):
	model = Order
	template_name = 'orderlist.html'

def OrderList(request):
	orders = Order.objects.all()
	return render(request,"orderlist.html",{'object_list':orders})

# def OrderCreate(request):
# 	if request.method == "POST":
# 		form = OrderForm(request.POST)
# 		if form.is_valid():
# 			try:
# 				form.save()
# 				model = form.instance
# 				return redirect('orderlist')
# 			except:
# 				pass
# 	else:
# 		form = OrderForm()
# 	return render(request,'ordercreate.html',{'form':form})

class OfferCreate(CreateView):
	form_class = OfferCreateForm
	success_url = '/order-list'

	# def get_success_url(self):
	# 	order = self.get_context_data()['order']
	# 	return redirect(f'order-detail/{order}')


class OrderCreate(CreateView):
	model = Order
	template_name = 'ordercreate.html'
	form_class = OrderCreateForm
	success_url = '/order-list'

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super().get_form_kwargs(*args, **kwargs)
		# kwargs['request'] = self.request
		kwargs.update({'request':self.request})
		return kwargs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.request.user
		context["user"] = user
		return context

class OrderDetail(DetailView):
	model = Order
	template_name = 'orderdetail.html'
	offer_create_form = OfferCreateForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user_pk = None
		if not self.request.user.is_anonymous: #and logist
			user_pk = self.request.user.pk

		context['offers'] = Offer.objects.filter(order=self.get_object().id)
		context['offer_create_form'] = self.offer_create_form(initial={'user':user_pk,
																	   'order': self.get_object().id})
		context['request'] = self.request
		# context['order'] =
		return context


def OrderUpdate(request, id):
	order = Order.objects.get(id=id)
	form = OrderForm(initial={'client': order.client.name,
							  'weightKG': order.weightKG,
							  'expectingPriceTenge': order.expectingPriceTenge,
							  'expectingDeliveryDate': order.expectingDeliveryDate})
	if request.method == "POST":
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			try:
				form.save()
				model = form.instance
				return redirect('/orderlist')
			except Exception as e:
				pass
	return render(request,'orderupdate.html',{'form':form})

def OrderDelete(request, id):
	order = Order.objects.get(id=id)
	try:
		order.delete()
	except:
		pass
	return redirect('orderlist')


def user_data(request):
	user = User.objects.all().count()
	logist = User.objects.filter(userprofile__user_type='logist').count()
	buyer = User.objects.filter(userprofile__user_type='buyer').count()


	return JsonResponse({
		'user_count':user,
		'logist_count': logist,
		'buyer': buyer,
		'percent': buyer/user
	}, safe=False)
