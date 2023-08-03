from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control,never_cache

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate,login,logout
from product.models import Color,Product
from variant.models import Variant,VariantImage
from category.models import category
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.password_validation import validate_password
# from .models import UserOTP
import re
import random
from django.conf import settings
import random
from django.core.mail import send_mail
from django.core.validators import validate_email

# Create your views here.
def home(request):
    categories = category.objects.all()
    products = Product.objects.all()
    variant_images = VariantImage.objects.order_by('variant__product').distinct('variant__product')
    variant_imagess = VariantImage.objects.order_by('variant__product__product_price').distinct('variant__product__product_price')
    variant_imaagess = VariantImage.objects.filter(variant__color__color_name='black').distinct()



    

    return render(request,'home.html', {'categories': categories, 'products': products,'variant_imagess': variant_imagess,'variant_imaagess':variant_imaagess, 'variant_images': variant_images})

def product_show(request,prod_id,img_id):
    
    variant = VariantImage.objects.filter(variant=img_id)
    variant_images = VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__product')
    color=VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__color')
    context={
        'variant':variant,
        'color':color,
        'variant_images' :variant_images,    
        # 'cart':cart
    }
    
    
    return render(request,'product/product_show.html',context)   

