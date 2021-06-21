from django.urls import path

from . import views

urlpatterns = [
    path('city/', views.CitiesListView.as_view(), name='city-list'),
    path('city/street/', views.CityStreetsListView.as_view(), name='get-streets'),
    path('shop/', views.ShopSet.as_view({'get': 'list', 'post': 'create'}), name='shop-interactions'),
]
