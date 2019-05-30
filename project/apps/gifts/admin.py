from django.contrib import admin

from . import models


@admin.register(models.Gift)
class Admin(admin.ModelAdmin):
	pass
