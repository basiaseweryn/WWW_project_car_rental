from django.contrib import admin
from django.utils.html import format_html

from .models import Car, City, RentalRecord


class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'city', 'year', 'dailyPrice', 'is_available', 'show_image')
    search_fields = ('brand', 'model')

    def show_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" />', obj.image.url)
        return "No Image"

    show_image.short_description = 'Image'

class CityAdmin(admin.ModelAdmin):
    list_display = ('city', 'country')

class RentalRecordAdmin(admin.ModelAdmin):
    list_display = ('account', 'car', 'start_date', 'end_date', 'total_price')

admin.site.register(Car, CarAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(RentalRecord, RentalRecordAdmin)