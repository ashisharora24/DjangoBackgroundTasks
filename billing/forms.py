from django import forms


class BillingForm(forms.Form):
    name = forms.CharField(max_length=120)
    number_1 = forms.IntegerField()
    number_2 = forms.IntegerField()
