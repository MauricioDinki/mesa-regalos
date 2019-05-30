import json

from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from project.apps.gifts.models import Gift
from project.apps.tables.models import Table, TableGift


class GiftsTableView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(GiftsTableView, self).dispatch(request, *args, **kwargs)

	def get(self, request):
		context = {'gifts': Gift.objects.all()}
		return TemplateResponse(request, 'gifts/add_to_table.html', context)

	def post(self, request):
		gifts = json.loads(request.POST.get('gifts'))
		table = Table.objects.filter(user=request.user).last()
		for gift in gifts:
			gift = Gift.objects.get(pk=gift)
			TableGift.objects.create(
				table=table,
				gift=gift
			)
		return HttpResponse('OK')


class UpdateGiftsTableView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(UpdateGiftsTableView, self).dispatch(request, *args, **kwargs)

	def get(self, request, **kwargs):
		context = {
			'gifts': Gift.objects.all(),
			'pk': kwargs.get('pk')
		}
		return TemplateResponse(request, 'gifts/update_gifts_table.html', context)

	def post(self, request, **kwargs):
		gifts = json.loads(request.POST.get('gifts'))
		table = Table.objects.get(pk=kwargs.get('pk'))
		tg = TableGift.objects.filter(table=table)
		for t in tg:
			t.delete()
		for gift in gifts:
			gift = Gift.objects.get(pk=gift)
			TableGift.objects.create(
				table=table,
				gift=gift
			)
		return HttpResponse('OK')
