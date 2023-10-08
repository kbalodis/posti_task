from django.urls import path
from . import views


urlpatterns = [
    path('', views.ApiOverview, name="Home"),
    path('parcel/create/', views.add_parcel, name="Add Parcel"),
    path('parcel/', views.view_parcels, name="Parcels"),
    path('parcel/update/<int:pk>/', views.update_parcel, name='Update Parcel'),
    path('parcel/delete/<int:pk>/', views.delete_parcel, name='Delete Parcel'),
    path('parcel_locker/create/', views.add_parcel_locker, name="Add Parcel Locker"),
    path('parcel_locker/', views.view_parcel_lockers, name="Parcel Lockers"),
    path('parcel_locker/update/<int:pk>/', views.update_parcel_locker, name='Update Parcel Locker'),
    path('parcel_locker/delete/<int:pk>/', views.delete_parcel_locker, name='Delete Parcel Locker'),
    path('putparceltolocker/<int:parcel>/<int:locker>/', views.put_parcel_to_locker, name='Put Parcel To Locker'),
    path('moveparcelbetweenlockers/<int:parcel>/<int:locker_src>/<int:locker_dest>/', 
         views.move_parcel_between_lockers, 
         name='Move Parcel Between Lockers'),
    path('takeparcelfromlocker/<int:parcel>/', views.take_parcel_from_locker, name='Take Parcel From Locker'),
]
