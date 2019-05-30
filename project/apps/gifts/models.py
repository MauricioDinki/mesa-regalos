from django.db import models
from django.utils.translation import gettext as _


class Gift(models.Model):
	name = models.CharField(
		verbose_name=_('Name'),
		blank=False,
		null=False,
		max_length=100
	)
	image = models.ImageField(
		verbose_name=_('Image'),
		blank=True,
		null=True,
	)
	price = models.FloatField(
		verbose_name=_('Price'),
		blank=False,
		null=False,
	)
	description = models.CharField(
		verbose_name=_('Description'),
		blank=False,
		null=False,
		max_length=100
	)
	stock = models.IntegerField(
		verbose_name=_('Stock'),
		blank=False,
		null=False,
	)

	class Meta:
		verbose_name = _('Gift')
		verbose_name_plural = _('Gifts')

	def __str__(self):
		return self.name
