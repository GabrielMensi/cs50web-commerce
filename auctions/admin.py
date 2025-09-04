from django.contrib import admin
from django import forms
from .models import User, Category, Listing, Comment, Bid
from .forms import BidFormSet


class BidInline(admin.StackedInline):
    model = Bid
    extra = 1
    formset = BidFormSet


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description', 
        'category',
        'owner',
        'starting_price',
        'current_price',
        'active'
    )
    readonly_fields = ('price', 'current_price')
    exclude = ('price',)  # Hide the FK price field - it's auto-managed
    inlines = [BidInline]
    
    def current_price(self, obj):
        """Show current price in admin list"""
        return obj.current_price
    current_price.short_description = 'Current Price'


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Bid)
