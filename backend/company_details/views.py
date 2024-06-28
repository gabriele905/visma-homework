from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse

from .forms import CompanyDetailDeleteBySymbolForm
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

        return qs.filter(f).order_by('symbol')


class CompanyDetailView(DetailView):
    model = CompanyDetail


class CompanyDetailCreate(CreateView):
    model = CompanyDetail
    fields = ['name', 'symbol']
    success_url = reverse_lazy('company_detail_list')

    def form_valid(self, form):
        return super().form_valid(form) \
            if CompanyDetail.validate_create_update_form(form) else super().form_invalid(form)


class CompanyDetailUpdate(UpdateView):
    model = CompanyDetail
    fields = ['name', 'symbol']
    success_url = reverse_lazy('company_detail_list')

    def form_valid(self, form):
        return super().form_valid(form) \
            if CompanyDetail.validate_create_update_form(form) else super().form_invalid(form)


class CompanyDetailDelete(DeleteView):
    model = CompanyDetail
    success_url = reverse_lazy('company_detail_list')


class CompanyDetailDeleteBySymbol(FormView):
    form_class = CompanyDetailDeleteBySymbolForm
    template_name = 'company_details/companydetail_delete_by_symbol_form.html'
    success_url = reverse_lazy('company_detail_list')

    def form_valid(self, form):
        symbol = form.cleaned_data['symbol'].upper()

        if not symbol:
            form.add_error('symbol', 'Symbol is required')
            return self.form_invalid(form)

        company = CompanyDetail.objects.filter(symbol=symbol).first()

        if not company:
            form.add_error('symbol', 'Company not found')
            return self.form_invalid(form)

        return redirect(reverse('company_detail_delete', kwargs={'pk': company.id}))
