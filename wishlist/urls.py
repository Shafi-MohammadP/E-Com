from django.urls import path
from . import views

urlpatterns = [
    path('wishlist', views.wishlist, name="wishlist"),
    path('add_wishlist', views.add_wishlist, name='add_wishlist'),
    path('wish_remove<int:remove_id>', views.wish_remove, name="wish_remove")
]
