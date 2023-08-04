from django.urls import path
from . import views

urlpatterns = [
    path('order_list/', views.order_list, name="order_list"),
    path('viewOrder/<int:view_id>/', views.viewOrder, name="viewOrder"),
    path('change_status', views.change_status, name="change_status")

]
