from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView, DeleteView, UpdateView, TemplateView

from project.apps.gifts.models import Gift
from project.apps.tables.forms import EventForm, BuyGiftForm
from project.apps.tables.models import Table, TableGift
from project.core.mixins import RequestFormMixin


class EventView(RequestFormMixin, FormView):
	template_name = 'events/create.html'
	form_class = EventForm
	success_url = reverse_lazy('gifts:gifts')

	def form_valid(self, form):
		form.save()
		return super(EventView, self).form_valid(form)


class TableDeleteView(DeleteView):
	model = Table
	template_name = 'tables/delete.html'
	success_url = reverse_lazy('users:profile')

	def get_object(self, queryset=None):
		""" Hook to ensure object is owned by request.user. """
		obj = super(TableDeleteView, self).get_object()
		if not obj.user == self.request.user:
			raise Http404
		return obj


class TableUpdate(RequestFormMixin, UpdateView):
	template_name = 'tables/update.html'
	form_class = EventForm
	success_url = reverse_lazy('users:profile')
	pk_url_kwarg = 'pk'

	def get_object(self, queryset=None):
		pk = self.kwargs.get('pk')
		obj = Table.objects.get(pk=pk)
		if not obj.user == self.request.user:
			raise Http404
		return obj


class TableDetailView(TemplateView):
	template_name = 'tables/detail.html'

	def get_context_data(self, **kwargs):
		context = super(TableDetailView, self).get_context_data(**kwargs)
		pk = kwargs.get('pk')
		obj = Table.objects.get(pk=pk)
		if not obj.user == self.request.user:
			raise Http404
		gifts = TableGift.objects.filter(table=obj)
		context['table'] = obj
		context['gifts'] = gifts
		return context


class SelectGiftView(View):
	def get_context_data(self, **kwargs):
		pk = kwargs.get('pk')
		table = Table.objects.get(pk=pk)
		gifts = TableGift.objects.filter(table=table)
		context = {
			'table': table,
			'gifts': gifts
		}
		return context

	def get(self, request, **kwargs):
		context = self.get_context_data(**kwargs)
		return TemplateResponse(request, 'tables/select.html', context)


class BuyGiftView(View):
	def get_context_data(self, **kwargs):
		table = Table.objects.get(pk=kwargs.get('pk'))
		gift = Gift.objects.get(pk=kwargs.get('id'))
		form = BuyGiftForm()
		context = {
			'table': table,
			'gift': gift,
			'form': form,
		}
		return context

	def get(self, request, **kwargs):
		context = self.get_context_data(**kwargs)
		return TemplateResponse(request, 'tables/buy.html', context)

	def post(self, request, **kwargs):
		context = self.get_context_data(**kwargs)
		buy_gift_form = BuyGiftForm(
			request.POST,
			request=request,
			table=context['table'],
			gift=context['gift'],
		)
		if buy_gift_form.is_valid():
			buy_gift_form.save()
			messages.info(request, "Felicidades, la compra fue completada con exito")
			return redirect(reverse_lazy('tables:select_gift', kwargs={'pk': kwargs.get('pk')}))
		context['form'] = buy_gift_form
		return TemplateResponse(request, 'tables/buy.html', context)