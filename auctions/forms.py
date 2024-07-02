from django import forms
from .models import Listing, Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid', 'user']


BidFormSet = forms.inlineformset_factory(Listing, Bid, form=BidForm, extra=1)
