#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.text import slugify


def eval_unique(data, model, field, error_message):
    """
    Function which evaluates unique data in models, useful for slugs,
    usernames etc.
    """
    original = data
    lookup = '%s__iexact' % field
    if field == 'slug':
        data = slugify(data)
        lookup = field
    try:
        model.objects.get(**{lookup: data})
    except model.DoesNotExist:
        return original
    raise forms.ValidationError(
        error_message
    )