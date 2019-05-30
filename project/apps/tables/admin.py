from django.contrib import admin

from . import models


@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
	list_display = ('name', 'user', 'date', 'get_type_display')
	list_filter = ('date', 'type')


@admin.register(models.TableGift)
class TableGiftAdmin(admin.ModelAdmin):
	list_display = ('table', 'gift', 'name', 'email')
	list_filter = ('table', 'gift')

admin.site.site_header = 'Mesa de Regalos'
admin.site.site_title = 'Mesa de Regalos'
