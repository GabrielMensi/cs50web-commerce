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
        'price',
        'active'
    )
    inlines = [BidInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        for formset in formsets:
            if formset.model == Bid:
                for form in formset:
                    bid = form.save(commit=False)
                    if not bid.listing:
                        bid.listing = form.instance
                    bid.save()
                form.instance.price = formset.instance
                form.instance.save()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:  # Es un nuevo objeto, excluye el campo price
            form.base_fields['price'].widget = forms.HiddenInput()
        return form


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment)
admin.site.register(Bid)
