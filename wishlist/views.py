from django.shortcuts import redirect, render
from product.models import Product,Color
from variant.models import Variant,VariantImage
# from user.models import CustomUser
from django.http import JsonResponse
from cart.models import Cart
from .models import Wishlist
from django.contrib.auth.decorators import login_required
# Create your views here.


def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).order_by('id')
        variants = wishlist.values_list('variant', flat=True)
        img = VariantImage.objects.filter(variant__in=variants).distinct('variant')

        context = {
            'wishlist': wishlist,
            'img': img,
        }
        return render(request,'wishlist/wishlist.html',context)
    else:
        return render(request,'wishlist/wishlist.html')



def add_wishlist(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            variant_id = request.POST.get('variant_id')
            print(variant_id, '65555555555555555555555555555555555')

            if Wishlist.objects.filter(user=request.user, variant_id=variant_id).exists():

                return JsonResponse({'status':'Product already in wishlist'})
            else:
                var =Variant.objects.get(id=variant_id)
                Wishlist.objects.create(user=request.user, variant=var)
            
                return JsonResponse({'status':'Product added successfully'})
        else:
            return JsonResponse({'status':'you are not login please login to continue'})
        
    return redirect('home')


# def add_wishlist(request):
#     if request.method =='POST':
#         if request.user.is_authenticated:
            
#             variant_id = request.POST.get('variant_id')
#             print(variant_id, '65555555555656665555555555555')
    
              
#             if Cart.objects.filter(user=request.user, variant_id=variant_id).exists():
                
#                 return JsonResponse({'status': 'Product already in cart'})
            
        
#             else:
#                 return JsonResponse({'status': 'Product added successfully'})
                
#         else:
#             return JsonResponse({'status': 'you are not login please Login to continue'})
            
            
#     return redirect('home')    