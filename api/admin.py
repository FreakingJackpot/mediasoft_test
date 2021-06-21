from django.contrib import admin

from .models import City, Street, Shop


# Register your models here.
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')
    list_filter = ('city',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'street', 'house', 'open', 'close')
    search_fields = ('name', 'city', 'street', 'house')
    list_filter = ('name', 'city', 'street')
