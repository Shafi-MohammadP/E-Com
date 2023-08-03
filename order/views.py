from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from checkout.models import Order,OrderItem
from userprofile.models import Address
from variant.models import Variant,VariantImage
from cart.models import Cart
from django.contrib import messages
from user.models import User
# Create your views here.


def order_list(request):
    user = request.user
    order =Order.objects.all()
    context={
        'order':order,
    }
    
    return render(request,'dashboard/order.html',context)

def viewOrder(request, view_id):
    
    try:
        orderview = Order.objects.get(id=view_id)
        address = Address.objects.get(id=orderview.address.id)
        products = OrderItem.objects.filter(order=view_id)
        variant_ids = [product.variant.id for product in products]
        image = VariantImage.objects.filter(variant__id__in=variant_ids).distinct('variant__product')
        context = {
            'orderview': orderview,
            'address': address,
            'products': products,
            'image' :image,

        }
    
            
            
            
        return render(request, 'view/order_view.html', context)
    except Order.DoesNotExist:
        print("Order does not exist")
    except Address.DoesNotExist:
        print("Address does not exist")
    return redirect('order_list')













