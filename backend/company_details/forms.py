from django import forms


class CompanyDetailDeleteBySymbolForm(forms.Form):
    symbol = forms.CharField(max_length=10, required=True)
