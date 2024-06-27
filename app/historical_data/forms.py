from django import forms

from company_details.models import CompanyDetail


class SyncHistoricalDataForm(forms.Form):
    date_from = forms.DateField(
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
    date_to = forms.DateField(
        required=True,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )
