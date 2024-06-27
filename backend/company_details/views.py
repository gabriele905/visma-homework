from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse

from backend.integrations.yahoo_finance import YahooFinanceClient

from .models import CompanyDetail


class CompanyDetailList(ListView):
    model = CompanyDetail
    paginate_by = 10

    def get_queryset(self):
        qs = super(CompanyDetailList, self).get_queryset()

        symbol = self.request.GET.get('symbol')

        f = Q()
        if symbol:
            f &= Q(symbol__contains=symbol.upper())

        return qs.filter(f).order_by('-symbol')


class CompanyDetailView(DetailView):
    model = CompanyDetail


class CompanyDetailCreate(CreateView):
    model = CompanyDetail
    fields = ['name', 'symbol']
    success_url = reverse_lazy('company_detail_list')

    def form_valid(self, form):
        symbol = form.cleaned_data['symbol'].upper()

        if CompanyDetail.objects.filter(symbol=symbol).exists():
            form.add_error('symbol', 'Company with this symbol already exists')
            return super().form_invalid(form)

        yfinance_client = YahooFinanceClient(symbol)
        if not yfinance_client.validate_ticker():
            form.add_error('symbol', 'Symbol is not valid')
            return super().form_invalid(form)

        form.instance.symbol = symbol

        return super().form_valid(form)


class CompanyDetailUpdate(UpdateView):
    model = CompanyDetail
    fields = ['name', 'symbol']
    success_url = reverse_lazy('company_detail_list')

    def form_valid(self, form):
        symbol = form.cleaned_data['symbol'].upper()

        if CompanyDetail.objects.filter(symbol=symbol).exclude(id=form.instance.id).exists():
            form.add_error('symbol', 'Company with this symbol already exists')
            return super().form_invalid(form)

        yfinance_client = YahooFinanceClient(symbol)
        if not yfinance_client.validate_ticker():
            form.add_error('symbol', 'Symbol is not valid')
            return super().form_invalid(form)

        form.instance.symbol = symbol

        return super().form_valid(form)


class CompanyDetailDelete(DeleteView):
    model = CompanyDetail
    success_url = reverse_lazy('company_detail_list')


class CompanyDetailDeleteBySymbol(FormView):
    model = CompanyDetail

    def form_valid(self, form):
        symbol = form.cleaned_data['symbol'].upper()

        if not symbol:
            messages.error(self.request, 'Symbol is required')
            return redirect('company_detail_list')

        company = CompanyDetail.objects.filter(id=symbol).first()

        if not company:
            messages.error(self.request, 'Company not found')
            return redirect('company_detail_list')

        return reverse('company_detail_delete', kwargs={'pk': company.id})
