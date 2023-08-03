from django.urls import path
from . import views

urlpatterns=[

    path('',views.admin_login1,name='admin_login1'),
    path('admin_signup',views.admin_signup,name='admin_signup'),
    path('usermanagement_1',views.usermanagement_1,name='usermanagement_1'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('admin_forgotpassword',views.admin_forgotpassword,name='admin_forgotpassword'),
    path('adminlogout', views.admin_logout1, name='admin_logout1'),
    path('userlisitng',views.users_listing, name='users_listing'),
    path('dashboardog', views.dashboardog, name='dashboardog'),  
    path('blockuser/<int:user_id>', views.blockuser, name='blockuser'),  
     
]