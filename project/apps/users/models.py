from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		"""Creates and saves a new user"""
		if not email:
			raise ValueError('Users must have an email address')
		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, password):
		"""Creates and saves a new superuser"""
		user = self.create_user(email, password)
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		user.save()

		return user


class User(AbstractBaseUser, PermissionsMixin):
	"""Custom user model that supports using email instead of username"""
	first_name = models.CharField(
		verbose_name=_('First Name'),
		max_length=255,
		blank=True,
		null=True
	)
	last_name = models.CharField(
		verbose_name=_('Last Name'),
		max_length=255,
		blank=True,
		null=True
	)
	email = models.EmailField(
		verbose_name=_('Email'),
		max_length=255,
		unique=True,
	)
	is_active = models.BooleanField(
		verbose_name=_('Is Active'),
		default=True
	)
	is_staff = models.BooleanField(
		verbose_name=_('Is Staff'),
		default=False
	)

	objects = UserManager()

	USERNAME_FIELD = 'email'

