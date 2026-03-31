from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),

    path('home/', views.home, name='home'),
    path('add/', views.add_activity, name='add'),

    path('farmer/', views.farmer_entry, name='farmer'),
    path('mill-entry/', views.mill_entry, name='mill_entry'),
    path('harvesting/', views.harvesting_page, name='harvesting'),
    path('harvest-farmer/', views.harvest_farmer, name='harvest_farmer'),
    path('harvester-entry/', views.harvester_entry, name='harvester_entry'),
     path('stats/', views.stats, name='stats'),
    path("notifications/", views.notifications, name="notifications"),
    path('account-management/', views.account_management, name='account_management'),
    path('profile/', views.profile, name='profile'),

    path('logout/', views.user_logout, name='logout'),

    path('aggregator/', views.aggregator, name='aggregator'),

 

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),






path('delete-mill/<int:id>/', views.delete_mill, name='delete_mill'),

path('delete-farmer/<int:id>/', views.delete_farmer, name='delete_farmer'),
path('delete-notification/<int:id>/', views.delete_notification, name='delete_notification'),
   
  
]

