from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from project.apps.gifts.models import Gift


class Table(models.Model):
	user = models.ForeignKey(
		get_user_model(),
		verbose_name=_('User'),
		blank=False,
		null=False,
		on_delete=models.CASCADE
	)
	name = models.CharField(
		verbose_name=_('Name'),
		blank=False,
		null=False,
		max_length=100
	)
	type = models.CharField(
		verbose_name=_('Type'),
		blank=False,
		null=False,
		max_length=100,
		choices=(
			('birthday', _('Birthday')),
			('christening', _('Christening')),
			('weeding', _('Weeding')),
			('fifteen_party', _('Fifteen Party')),
		)
	)
	date = models.DateField(
		verbose_name=_('Date'),
		blank=False,
		null=False
	)
	close_date = models.DateField(
		verbose_name=_('Close Date'),
		blank=False,
		null=False
	)
	delivery_date = models.DateField(
		verbose_name=_('Delivery Date'),
		blank=False,
		null=False
	)
	description = models.TextField(
		verbose_name=_('Description'),
		blank=False,
		null=False
	)

	class Meta:
		verbose_name = _('Table')
		verbose_name_plural = _('Tables')

	def __str__(self):
		return self.name


class TableGift(models.Model):
	table = models.ForeignKey(
		Table,
		verbose_name=_('Table'),
		blank=False,
		null=False,
		on_delete=models.CASCADE
	)
	gift = models.ForeignKey(
		Gift,
		verbose_name=_('Gift'),
		blank=False,
		null=False,
		on_delete=models.CASCADE
	)
	name = models.CharField(
		verbose_name=_('Name'),
		blank=True,
		null=True,
		max_length=100
	)
	email = models.CharField(
		verbose_name=_('Email'),
		blank=True,
		null=True,
		max_length=100
	)
	note = models.TextField(
		verbose_name=_('Note'),
		blank=True,
		null=True,
	)

	class Meta:
		verbose_name = _('Table Gift')
		verbose_name_plural = _('Table Gifts')

	def __str__(self):
		return "%s %s" % (self.table.name, self.gift.name)
