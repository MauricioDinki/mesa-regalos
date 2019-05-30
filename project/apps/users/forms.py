from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from project.core import validators


class SignupForm(forms.Form):
	first_name = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'placeholder': _('First Name')
			}
		),
	)
	last_name = forms.CharField(
		widget=forms.TextInput(
			attrs={
				'placeholder': _('Last Name')
			}
		),
	)
	email = forms.EmailField(
		widget=forms.EmailInput(
			attrs={
				'placeholder': _('Email')
			}
		),
	)
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'placeholder': _('Password')
			}
		),
	)

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		self.request = kwargs.pop('request', None)
		super(SignupForm, self).__init__(*args, **kwargs)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		error_message = _('This email is already associated with an account')
		return validators.eval_unique(email, get_user_model(), 'email', error_message)

	def save(self):
		cleaned_data = super(SignupForm, self).clean()

		user = get_user_model().objects.create(
			email=cleaned_data.get('email'),
			first_name=cleaned_data.get('first_name'),
			last_name=cleaned_data.get('last_name'),
		)

		user.set_password(cleaned_data.get('password'))

		user.save()

		self.user_cache = authenticate(
			username=cleaned_data.get('email'),
			password=cleaned_data.get('password'),
		)


class LoginForm(forms.Form):
	username = forms.CharField(
		widget=forms.EmailInput(
			attrs={
				'class': 'form-control',
				'placeholder': _('Email')
			}
		),
		label=''
	)

	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
				'class': 'form-control',
				'placeholder': _('Password')
			}
		),
		label=''
	)

	def __init__(self, *args, **kwargs):
		self.user_cache = None
		super(LoginForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].required = True

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if username and password:
			self.user_cache = authenticate(
				username=username, password=password
			)
			if self.user_cache is None:
				raise forms.ValidationError(
					_('Email or password are incorrect'),
				)
			elif not self.user_cache.is_active:
				raise forms.ValidationError(
					_('This account is not active')
				)
		return self.cleaned_data
