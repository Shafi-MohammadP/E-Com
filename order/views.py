from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from checkout.models import Order, OrderItem, Orderstatus, Itemstatus
from userprofile.models import Address
from variant.models import Variant, VariantImage
from cart.models import Cart
from django.contrib import messages
from user.models import User
from django.contrib import messages
# Create your views here.


def order_list(request):
    user = request.user
    order = Order.objects.all()
    context = {
        'order': order,
    }

    return render(request, 'dashboard/order.html', context)


def viewOrder(request, view_id):

    try:
        orderview = Order.objects.get(id=view_id)
        address = Address.objects.get(id=orderview.address.id)
        products = OrderItem.objects.filter(order=view_id)
        variant_ids = [product.variant.id for product in products]
        image = VariantImage.objects.filter(
            variant__id__in=variant_ids).distinct('variant__product')
        item_status_o = Itemstatus.objects.all()
        context = {
            'orderview': orderview,
            'address': address,
            'products': products,
            'image': image,
            'item_status_o': item_status_o,

        }

        return render(request, 'view/order_view.html', context)
    except Order.DoesNotExist:
        print("Order does not exist")
    except Address.DoesNotExist:
        print("Address does not exist")
    return redirect('order_list')


def change_status(request):

    if not request.user.is_authenticated:
        return redirect('admin_login1')

    orderitem_id = request.POST.get('orderitem_id')
    order_status = request.POST.get('status')
    order_variant = request.POST.get('variant_id')

    orderitems = OrderItem.objects.get(variant=order_variant, id=orderitem_id)
    item_status_instance = Itemstatus.objects.get(id=order_status)

    orderitems.orderitem_status = item_status_instance
    orderitems.save()
    view_id = orderitems.order.id

    all_order_items = OrderItem.objects.filter(order=view_id)
    print(all_order_items, '11111111111111111111111111111111111111')
    Pending = 0
    Processing = 0
    Shipped = 0
    Delivered = 0
    Cancelled = 0
    Return = 0

    for i in all_order_items:
        # Pending
        if i.orderitem_status.id == 1:
            Pending += 1
        # Processing
        if i.orderitem_status.id == 2:
            Processing += 1
        # Shipped

        if i.orderitem_status.id == 3:
            Shipped += 1
        # Delivered
        if i.orderitem_status.id == 4:
            Delivered += 1
        # Cancelled
        if i.orderitem_status.id == 5:
            Cancelled += 1
        # Return
        if i.orderitem_status.id == 6:
            Return += 1

    total_items = len(all_order_items)
    print(total_items, '65555555555555555555555555555555555555555')

    total_value = 1
    if total_items == Pending:
        total_value = 1
    elif total_items == Processing:
        total_value = 2
    elif total_items == Shipped:
        total_value = 3
    elif total_items == Delivered:
        total_value = 4
    elif total_items == Cancelled:
        total_value = 5
    elif total_items == Return:
        total_value = 6

    change_all_items_status = Order.objects.get(id=view_id)
    item_status_instance_all = Orderstatus.objects.get(id=total_value)
    change_all_items_status.order_status = item_status_instance_all
    change_all_items_status.save()

    messages.success(request, 'status updated')
    return redirect('order_list')
