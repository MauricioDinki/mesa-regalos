#!/usr/bin/python
# -*- coding: utf-8 -*-

from .base import *

# DEBUG
# -----------------------------------------------------------------------------

SECRET_KEY = env(
	"DJANGO_SECRET_KEY",
	default="pkKvvaquTxQfVyBFlSIwht5sj2wZy4M4vocucuvrMaTYpdAOedHYpheN9JKzSzHv",
)
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']