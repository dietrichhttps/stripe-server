from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency', 'description')
    list_filter = ('currency',)
    search_fields = ('name', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_price', 'currency', 'discount', 'tax', 'created_at')
    list_filter = ('discount', 'tax', 'created_at')
    filter_horizontal = ('items',)
    readonly_fields = ('created_at',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent_off', 'stripe_coupon_id')
    search_fields = ('name', 'stripe_coupon_id')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'stripe_tax_rate_id')
    search_fields = ('name', 'stripe_tax_rate_id')
