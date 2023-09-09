from checkout.models import Order, OrderItem
from django.shortcuts import redirect
from django.contrib import messages
from fpdf import FPDF
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_control, never_cache

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.text import slugify
from django.db.models import OuterRef, Subquery
from cart.models import Cart
from wishlist.models import Wishlist
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.loader import get_template
from fpdf import FPDF
from io import BytesIO

# verification email
import re
import random
from django.conf import settings
import random
from checkout.models import Order, OrderItem, Orderstatus, Itemstatus
# from checkout.models import Order, OrderItem
from .models import Address, Wallet
from django.core.mail import send_mail
from django.core.validators import validate_email
from user.models import User
from category.models import category
from variant.models import Variant, VariantImage
from django.contrib.auth import update_session_auth_hash
# Create your views here.


@login_required(login_url='user_login1')
def userprofile(request):
    user = request.user
    categories = category.objects.all()
    addresses = Address.objects.filter(user=request.user, is_available=True)
    orders = Order.objects.filter(user=request.user)
    walletamount = Wallet.objects.filter(user=request.user)
    print(walletamount, '546sdfffffffffffffffffff')
    try:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count = False
        wishlist_count = False

    # try:

    #     walletamount = Wallet.objects.filter(user=request.user)
    # except Wallet.DoesNotExist:
    #     walletamount = 0
    context = {
        'user': user,
        'addresses': addresses,
        'orders': orders,
        'walletamount': walletamount,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
    }
    return render(request, 'userprofile/userprofile.html', context)


def add_address(request, check_id):
    if request.method == 'POST':
        # Code for processing form data and validation
        # ...
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')

        if request.user is None:
            return

        if first_name.strip() == '':
            messages.error(request, 'names cannot be empty!!!')
            return render(request, 'userprofile/add_address.html', )

        if last_name.strip() == '':
            messages.error(request, 'names cannot be empty!!!')
            return render(request, 'userprofile/add_address.html', )

        if country.strip() == '':
            messages.error(request, 'Country cannot be empty')
            return render(request, 'userprofile/add_address.html', )

        if city.strip() == '':
            messages.error(request, 'city cannot be empty')
            return render(request, 'userprofile/add_address.html', )

        if address.strip() == '':
            messages.error(request, 'address cannot be empty')
            return render(request, 'userprofile/add_address.html', )

        if pincode.strip() == '':
            messages.error(request, 'pincode cannot be empty')
            return render(request, 'userprofile/add_address.html', )

        if not re.search(re.compile(r'^\d{6}$'), pincode):
            messages.error(request, 'should only 6 contain numeric!')
            return render(request, 'userprofile/add_address.html', )

        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), phone):
            messages.error(request, 'Enter valid phonenumber!')
            return render(request, 'userprofile/add_address.html', )

        if phone.strip() == '':
            messages.error(request, 'phone cannot be empty')
            return render(request, 'userprofile/add_address.html', )

        if email.strip() == '':
            messages.error(request, 'email cannot be empty')
            return render(request, 'userprofile/add_address.html', )

        email_check = validateemail(email)
        if email_check is False:
            messages.error(request, 'email not valid!')

            return render(request, 'userprofile/add_address.html', )

        if state.strip() == '':
            messages.error(request, 'state cannot be empty')

            return render(request, 'userprofile/add_address.html', )

        # After validation, create and save the address object
        ads = Address()
        ads.user = request.user
        ads.first_name = first_name
        ads.last_name = last_name
        ads.country = country
        ads.address = address
        ads.city = city
        ads.pincode = pincode
        ads.phone = phone
        ads.email = email
        ads.state = state
        ads.is_available = True
        ads.save()
        messages.success(request, 'Address added succesfully')

        if check_id == 1:
            check = 1
            return redirect('userprofile')
        else:
            check = 2
            return redirect('checkout')

    if check_id == 1:
        check = 1
    else:
        check = 2

    return render(request, 'userprofile/add_address.html', {'check': check})


def edit_address(request, edit_id):

    if request.method == 'POST':

        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        state = request.POST.get('state')
        try:
            editaddress = Address.objects.get(id=edit_id)
        except:
            return redirect('userprofile')

        context = {
            'pre_first_name': first_name,
            'pre_last_name': last_name,
            'pre_country': country,
            'pre_address': address,
            'pre_city': city,
            'pre_ pincode': pincode,
            'pre_phone': phone,
            'pre_email': email,
            'pre_state': state,
            'edit_id': edit_id,

        }

        if request.user is None:
            return

        if first_name.strip() == '':
            messages.error(request, 'names cannot be empty!!!')
            context['pre_first_name'] = ''
            return redirect('edit_address', {'editaddress': editaddress})

        if last_name.strip() == '':
            messages.error(request, 'names cannot be empty!!!')
            context['pre_last_name'] = ''
            return redirect('edit_address', {'editaddress': editaddress})

        if country.strip() == '':
            messages.error(request, 'Country cannot be empty')
            context['pre_country'] = ''
            return redirect('edit_address', {'editaddress': editaddress})
        if city.strip() == '':
            messages.error(request, 'city cannot be empty')
            context['pre_city'] = ''
            return redirect('edit_address', {'editaddress': editaddress})
        if address.strip() == '':
            messages.error(request, 'address cannot be empty')
            context['pre_address'] = ''
            return redirect('edit_address', {'editaddress': editaddress})
        if pincode.strip() == '':
            messages.error(request, 'pincode cannot be empty')
            context['pre_ pincode'] = ''
            return redirect('edit_address', {'editaddress': editaddress})
        if not re.search(re.compile(r'^\d{6}$'), pincode):
            messages.error(request, 'should only 6 contain numeric!')
            context['pre_ pincode'] = ''
            return redirect('edit_address', {'editaddress': editaddress})
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), phone):
            messages.error(request, 'Enter valid phonenumber!')
            context['pre_phone'] = ''
            return redirect('edit_address', {'editaddress': editaddress})
        if phone.strip() == '':
            messages.error(request, 'phone cannot be empty')
            context['pre_phone'] = ''
            return redirect('edit_address', {'editaddress': editaddress})
        if email.strip() == '':
            messages.error(request, 'email cannot be empty')
            context['pre_email'] = ''
            return redirect('edit_address', {'editaddress': editaddress})
        email_check = validateemail(email)
        if email_check is False:
            messages.error(request, 'email not valid!')
            context['pre_email'] = ''
            return redirect('edit_address', {'editaddress': editaddress})

        if state.strip() == '':
            messages.error(request, 'state cannot be empty')
            context['pre_state'] = ''
            return redirect('edit_address', {'editaddress': editaddress})

        try:
            ads = Address.objects.get(id=edit_id)
        except Address.DoesNotExist:
            messages.error(request, 'Address not found!')
            return redirect('userprofile')

        ads.user = request.user
        ads.first_name = first_name
        ads.last_name = last_name
        ads.country = country
        ads.address = address
        ads.city = city
        ads.pincode = pincode
        ads.phone = phone
        ads.email = email
        ads.state = state
        ads.is_available = True
        ads.save()
        messages.success(request, 'Address edited succesfully')
        return redirect('userprofile')
    else:
        try:
            editaddress = Address.objects.get(id=edit_id)
        except:
            return redirect('userprofile')

        return render(request, 'userprofile/edit_address.html', {'editaddress': editaddress})


def editprofile(request):

    return render(request, 'userprofile/edit_profile.html')


def deleteaddress(request, delete_id):
    address = Address.objects.get(id=delete_id)
    address.is_available = False
    address.save()
    messages.success(request, ' Address deleted successfully!')

    return redirect('userprofile')


def viewaddress(request, view_id):
    try:
        Viewaddress = Address.objects.get(id=view_id)
    except:
        return redirect('userprofile')

    return render(request, 'userprofile/view_address.html', {'Viewaddress': Viewaddress})


def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        try:
            user = request.user
        except:
            return redirect('userprofile')

        # print(phone_number,first_name)

        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request, 'First or Lastname is empty')
            return render(request, 'userprofile/edit_profile.html', {'user': user})
        if email.strip() == '':
            messages.error(request, 'email cannot be empty')
            return render(request, 'userprofile/edit_profile.html', {'user': user})
        email_check = validateemail(email)
        if email_check is False:
            messages.error(request, 'email not valid!')
            return render(request, 'userprofile/edit_profile.html', {'user': user})

        try:
            user = request.user
            print(user.first_name, '222222222222222222222222222222222222222222222')

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, 'userprofile updated successfully')
            return redirect('userprofile')

        except:
            messages.error(request, 'User does not exist')
    try:
        user = User.objects.get(email=request.user)
    except:
        return redirect('userprofile')
    return render(request, 'userprofile/edit_profile.html', {'user': user})


def change_password(request):

    if request.method == 'POST':

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password.strip() == '' or confirm_password.strip() == '':
            messages.error(request, 'Field Cannot Empty')
            return render(request, 'userprofile/password.html')

        if new_password != confirm_password:
            messages.error(request, 'Password Does not Match')
            return render(request, 'userprofile/password.html')

        passwordcheck = validate_password(new_password)
        if passwordcheck is False:
            messages.error(request, 'Enter Strong Password')
            return render(request, 'userprofile/password.html')

        user = request.user

        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Password Changed Succesfully')
            return redirect('userprofile')
        else:
            messages.error(request, 'Invalid old password')
            return render(request, 'userprofile/password.html')
    return render(request, 'userprofile/password.html')


def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validatepassword(new_password):
    try:
        validate_password(new_password)
        return True
    except ValidationError:
        return False


# def order_detail_view(request, order_id):
#     try:
#         orderview = Order.objects.get(id=order_id)
#         address = Address.objects.get(id=orderview.address.id)
#         products = OrderItem.objects.filter(order=order_id)
#         variant_ids = [product.variant.id for product in products]
#         image = VariantImage.objects.filter(
#             variant__id__in=variant_ids).distinct('variant__product')
#         item_status_o = Itemstatus.objects.all()
#         orders = Order.objects.filter(user=request.user)
#         context = {
#             'orderview': orderview,
#             'address': address,
#             'products': products,
#             'image': image,
#             'item_status_o': item_status_o,
#             'orders': orders,

#         }

#         return render(request, 'userprofile/order_detail.html', context)
#     except Order.DoesNotExist:
#         print("Order does not exist")
#     except Address.DoesNotExist:
#         print("Address does not exist")
#     return redirect('userprofile')

# def order_detail_view(request, order_id):
#     try:
#         orderview = Order.objects.get(id=order_id)
#         address = Address.objects.get(id=orderview.address.id)
#         products = OrderItem.objects.filter(order=order_id)

#         # Collect all variant IDs for the products in the order
#         variant_ids = [product.variant.id for product in products]

#         # Retrieve variant images for the collected variant IDs
#         # This will give you images for all color variants of the products
#         images = VariantImage.objects.filter(variant__id__in=variant_ids)

#         item_status_o = Itemstatus.objects.all()
#         orders = Order.objects.filter(user=request.user)

#         context = {
#             'orderview': orderview,
#             'address': address,
#             'products': products,
#             'images': images,  # Changed 'image' to 'images'
#             'item_status_o': item_status_o,
#             'orders': orders,
#         }

#         return render(request, 'userprofile/order_detail.html', context)
#     except Order.DoesNotExist:
#         print("Order does not exist")
#     except Address.DoesNotExist:
#         print("Address does not exist")
#     return redirect('userprofile')


# def order_detail_view(request, order_id):
#     try:
#         orderview = Order.objects.get(id=order_id)
#         address = Address.objects.get(id=orderview.address.id)
#         products = OrderItem.objects.filter(order=order_id)

#         # Fetch the first image for each variant using a subquery
#         image_subquery = VariantImage.objects.filter(
#             variant=OuterRef('variant')).order_by('id')
#         products_with_images = products.annotate(
#             first_image=Subquery(image_subquery.values('image')[:1]))

#         item_status_o = Itemstatus.objects.all()
#         orders = Order.objects.filter(user=request.user)

#         context = {
#             'orderview': orderview,
#             'address': address,
#             'products': products_with_images,
#             'item_status_o': item_status_o,
#             'orders': orders,
#         }

#         return render(request, 'userprofile/order_detail.html', context)
#     except Order.DoesNotExist:
#         print("Order does not exist")
#     except Address.DoesNotExist:
#         print("Address does not exist")
#     return redirect('userprofile')

def order_detail_view(request, view_id):
    try:
        orderview = Order.objects.get(id=view_id)
        address = Address.objects.get(id=orderview.address.id)
        products = OrderItem.objects.filter(order=view_id)
        variant_ids = [product.variant.id for product in products]
        for i in variant_ids:
            print(i, 'jhikkkkkkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
        print(variant_ids, 'sdffffffffffffffffffffffffffffffffffffffffffff')
        image = VariantImage.objects.filter(
            variant__id__in=variant_ids).distinct('variant__color')
        item_status_o = Itemstatus.objects.all()
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        context = {
            'orderview': orderview,
            'address': address,
            'products': products,
            'image': image,
            'item_status_o': item_status_o,
            'wishlist_count': wishlist_count,
            'cart_count': cart_count,

        }
        return render(request, 'userprofile/order_detail.html', context)

    except Order.DoesNotExist:
        print("Order does not exist")
    except Address.DoesNotExist:
        print("Address does not exist")
    return redirect('userprofile')
 # You'll need to install xhtml2pdf library


def download_invoice(request, view_id):
    try:
        # Retrieve the order based on view_id
        order = Order.objects.get(id=view_id)

        # Retrieve related order items
        order_items = OrderItem.objects.filter(order=order)

        # Create a PDF document
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 12)
                self.cell(0, 10, 'Invoice', align='C', ln=True)

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)

        # Add order details
        pdf.cell(0, 10, f'Order ID: {order.id}', ln=True)
        pdf.cell(0, 10, f'Order Date: {order.created_at}', ln=True)
        pdf.cell(0, 10, f'Total Amount: ${order.total_price}', ln=True)
        pdf.cell(0, 10, f'Payment Mode: {order.payment_mode}', ln=True)

        # Add a table for order items
        pdf.ln(10)  # Move down to create space before the table
        # Set background color for header row
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(60, 10, 'Product Name', 1, 0, 'C', 1)  # Header: Product Name
        pdf.cell(30, 10, 'Price', 1, 0, 'C', 1)  # Header: Price
        pdf.cell(30, 10, 'Quantity', 1, 0, 'C', 1)  # Header: Quantity
        pdf.cell(40, 10, 'Subtotal', 1, 1, 'C', 1)  # Header: Subtotal

        # Add order item rows
        for item in order_items:
            # Product Name
            pdf.cell(60, 10, item.variant.product.product_name, 1)
            pdf.cell(30, 10, f'${item.price}', 1)  # Price
            pdf.cell(30, 10, str(item.quantity), 1)  # Quantity
            # Subtotal
            pdf.cell(40, 10, f'${item.price * item.quantity}', 1, 1)

        # Generate PDF content as bytes
        pdf_bytes = pdf.output(dest='S').encode('latin1')

        # Create an HttpResponse with the PDF content
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{view_id}.pdf"'

        return response

    except Order.DoesNotExist:
        messages.error(request, 'Order does not exist')
        return redirect('userprofile')

    # Handle any other exceptions or errors as needed


# def download_invoice(request, order_id):
#     # Generate the invoice content (HTML or PDF)

#     invoice_content = render_to_string(
#         'userprofile/invoice_template.html', {'order_id': order_id})

#     # Convert the HTML to PDF (you may need to use a library for this)
#     # For simplicity, let's assume the invoice_content is already in PDF format

#     # Create a response with the PDF content
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="invoice_{slugify(order_id)}.pdf"'
#     response.write(invoice_content)

#     return response
