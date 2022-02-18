from django.shortcuts import  render, redirect
from django.views.generic import ListView, CreateView, DetailView

from .forms import NewUserForm, OrderForm, OrderCreateForm
from django.contrib.auth import login
from django.contrib import messages

from .models import Order


def register_request(request):
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

class OrderCreate(CreateView):
	model = Order
	template_name = 'ordercreate.html'
	form_class = OrderCreateForm
	success_url = '/'

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