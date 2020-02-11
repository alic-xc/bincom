from django import forms

class PollingUnitForm(forms.Form):
    unit_number = forms.CharField(required=True, max_length=10, widget=forms.TextInput(attrs={
        'placeholder': 'Enter polling unit number'
    }))


class PollingResultForm(forms.Form):
    polling_unit = forms.CharField(required=True, max_length=10)
    party_name = forms.CharField(required=True, max_length=20)
    party_score = forms.IntegerField(required=True, max_value=20000)
    



class PlainForm(forms.Form):
    pass