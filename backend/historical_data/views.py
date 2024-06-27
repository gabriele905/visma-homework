import csv

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, ListView
from django.urls import reverse_lazy

from backend.company_details.models import CompanyDetail

from .forms import SyncHistoricalDataForm
from .models import HistoricalData


class HistoricalDataList(ListView):
    model = HistoricalData

    def get_queryset(self):
        qs = super(HistoricalDataList, self).get_queryset()

        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')

        date_filter = Q()
        if date_from:
            date_filter &= Q(date__gte=date_from)
        if date_to:
            date_filter &= Q(date__lte=date_to)

        f = date_filter & Q(company=self.kwargs['company_id'])

        return qs.filter(f).order_by('-date')

    def get_context_data(self, **kwargs):
        company = CompanyDetail.objects.filter(id=self.kwargs['company_id']).first()
        context = super().get_context_data(**kwargs)
        context["company"] = company

        return context

    def export_csv(self):
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="file.csv"'},
        )

        writer = csv.writer(response)

        for obj in self.get_queryset():
            writer.writerow([obj.date, obj.open, obj.high, obj.low, obj.close, obj.adj_close, obj.volume])

        return response

    def get(self, request, *args, **kwargs):
        if 'csv' in request.GET:
            return self.generate_csv()

        return super(HistoricalDataList, self).get(request, *args, **kwargs)

    def generate_csv(self):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="name_of_csv_download.csv"'

        csv_fields = HistoricalData.get_csv_fields()

        writer = csv.writer(response)
        writer.writerow([field_name for field_name in csv_fields])

        for row in self.get_queryset():
            writer.writerow([getattr(row, field_name) for field_name in csv_fields])

        return response


class HistoricalDataSync(FormView):
    template_name = "historical_data/sync_data_form.html"
    form_class = SyncHistoricalDataForm

    def get_success_url(self):
        return reverse_lazy('company_historical_data_view', kwargs={'company_id': self.kwargs['company_id']})

    def form_valid(self, form):
        date_from = form.cleaned_data['date_from']
        date_to = form.cleaned_data['date_to']

        if date_from > date_to:
            form.add_error('date_to', 'The "to" date must be later than the "from" date')
            return super().form_invalid(form)

        company = CompanyDetail.objects.filter(id=self.kwargs['company_id']).first()

        if not company:
            messages.error(self.request, 'Company not found')
            return redirect('company_detail_list')

        if not company.download_data(date_from, date_to):
            form.add_error(None, 'Failed to download data')
            return super().form_invalid(form)

        return super().form_valid(form)
