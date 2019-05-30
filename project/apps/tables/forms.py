from datetime import timedelta, date
import random

from django import forms
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.utils.translation import gettext as _
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as can


from project.apps.tables.models import Table, TableGift


class EventForm(forms.ModelForm):
	date = forms.DateField(
		widget=forms.TextInput(
			attrs={'type': 'date'}
		)
	)

	class Meta:
		model = Table
		fields = ('name', 'type', 'date', 'description',)

	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop('request', None)
		super(EventForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		m = super(EventForm, self).save(commit=False)
		m.user = self.request.user
		m.close_date = self.cleaned_data.get('date') + timedelta(days=7)
		m.delivery_date = self.cleaned_data.get('date') + timedelta(days=14)
		if commit:
			m.save()
		return m


class BuyGiftForm(forms.Form):
	name = forms.CharField(
		widget=forms.TextInput(),
		label=_('Name')
	)
	email = forms.EmailField(
		widget=forms.EmailInput(),
		label=_('Email')
	)
	note = forms.CharField(
		widget=forms.Textarea(
			attrs={
				'placeholder': _('You can write a note with your gift')
			}
		),
		label=_('Note')
	)
	card_number = forms.IntegerField(
		widget=forms.TextInput(),
		label=_('Card Number')
	)
	expiration_month = forms.IntegerField(
		widget=forms.TextInput(),
		label=_('Expiration Month (MM)')

	)
	expiration_year = forms.IntegerField(
		widget=forms.TextInput(),
		label=_('Expiration Year (YY)')
	)
	cvv2 = forms.IntegerField(
		widget=forms.TextInput(),
		label=_('CVV')
	)
	address = forms.CharField(
		widget=forms.TextInput(),
		help_text=_('Just if you require bill'),
		label=_('Address'),
		required=False
	)
	rfc = forms.CharField(
		widget=forms.TextInput(),
		help_text=_('Just if you require bill'),
		label=_('RFC'),
		required=False
	)

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		self.request = kwargs.pop('request', None)
		self.table = kwargs.pop('table', None)
		self.gift = kwargs.pop('gift', None)
		super(BuyGiftForm, self).__init__(*args, **kwargs)

	def clean(self):
		cleaned_data = super(BuyGiftForm, self).clean()
		if self.gift.stock <= 0:
			raise ValidationError('This product is not available, try with another')
		return cleaned_data

	def save(self):
		cleaned_data = super(BuyGiftForm, self).clean()
		name = cleaned_data.get('name')
		email = cleaned_data.get('email')
		note = cleaned_data.get('email')
		address = cleaned_data.get('address')
		rfc = cleaned_data.get('address')

		tablegift = TableGift.objects.get(
			table=self.table,
			gift=self.gift
		)

		tablegift.name = name
		tablegift.email = email
		tablegift.note = note
		tablegift.save()

		self.gift.stock -= 1
		self.gift.save()

		if address and rfc:
			today = date.today().strftime("%d/%m/%Y")

			canvas = can.Canvas("/tmp/form.pdf", pagesize=letter)
			canvas.setLineWidth(.3)
			canvas.setFont('Helvetica', 12)

			canvas.drawString(30, 750, 'REGALOS S.A de CV')
			canvas.drawString(30, 735, 'FACTURA #%s' % random.randint(1, 1000))
			canvas.drawString(500, 750, today)
			canvas.line(480, 747, 580, 747)

			canvas.drawString(30, 703, 'RFC de REGALOS S.A de CV:')
			canvas.drawString(230, 703, "SAVR090503795")

			canvas.drawString(30, 683, 'Direccion de REGALOS S.A de CV:')
			canvas.drawString(230, 683, "AV JUAREZ NO. 907, PERIODISTAS, 42000, Pachuca, HIDALGO")

			canvas.drawString(30, 643, 'Nombre:')
			canvas.drawString(230, 643, name)

			canvas.drawString(30, 623, 'RFC:')
			canvas.drawString(230, 623, rfc)

			canvas.drawString(30, 603, 'Direcciom:')
			canvas.drawString(230, 603, address)

			canvas.drawString(30, 583, 'Importe:')
			canvas.drawString(230, 583, "%s" % int(self.gift.price) ** 0.84)

			canvas.drawString(30, 563, 'IVA:')
			canvas.drawString(230, 563, "%s" % int(self.gift.price) ** 0.16)

			canvas.drawString(30, 543, 'TOTAL:')
			canvas.drawString(230, 543, "%s" % int(self.gift.price))

			canvas.save()

			email = EmailMessage()
			email.subject = "La factura de tu regalo esta lista"
			email.body = "Muchas gracias por tu compra"
			email.from_email = "cuentatest997@gmail.com"
			email.to = [email]
			email.attach_file("/tmp/form.pdf")
			email.send()


