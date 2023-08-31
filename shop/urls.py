from django.urls import path
from .import views

urlpatterns = [
    path('shop_filter', views.Shop_Filtering, name='Shop_Filter'),
    path('category_filtering<int:cate_id>/',
         views.category_filtering, name="catefilter")
]
