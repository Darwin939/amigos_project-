from django.urls import path
from . import views

app_name = "admin_analytics_service"


urlpatterns = [
    path("", views.index, name="homepage"),
    path("register/", views.register_request, name="register"),
    path("register_logist/", views.register_logist_request, name="register_logist"),
    path('order-list', views.OrderList, name='orderlist'),
    path('order-create', views.OrderCreate.as_view(), name='ordercreate'),
    path('order-update/<int:id>', views.OrderUpdate, name='orderupdate'),
    path('order-delete/<int:id>', views.OrderDelete, name='orderdelete'),
    path('order-detail/<int:pk>', views.OrderDetail.as_view(), name='orderdetail'),
    path('offer_create', views.OfferCreate.as_view(), name='offercreate'),


]