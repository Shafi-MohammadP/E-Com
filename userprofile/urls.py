from django.urls import path
from . import views

urlpatterns=[

  
    path('',views.userprofile,name='userprofile'),
    path('add_address',views.add_address,name='add_address'),
    path('edit_address/<int:edit_id>/', views.edit_address, name='edit_address'),
    path('deleteaddress/<int:delete_id>/',views.deleteaddress,name='deleteaddress'),
    path('view_address/<int:view_id>/', views.viewaddress, name='viewaddress'),
    path("editprofilee", views.editprofile, name="editprofile"),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name="change_password")
    
   
]