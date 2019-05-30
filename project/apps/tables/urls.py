from django.conf.urls import url

from . import views

app_name = 'tables'

urlpatterns = [
	url(regex=r'^evento/$', view=views.EventView.as_view(),
		name='event'),

	url(regex=r'^mesas/(?P<pk>[-\w]+)/$', view=views.TableDetailView.as_view(),
		name='detail_table'),

	url(regex=r'^mesas/(?P<pk>[-\w]+)/comprar/$', view=views.SelectGiftView.as_view(),
		name='select_gift'),

	url(regex=r'^mesas/(?P<pk>[-\w]+)/comprar/(?P<id>[-\w]+)/$', view=views.BuyGiftView.as_view(),
		name='buy_gift'),

	url(regex=r'^mesas/eliminar/(?P<pk>[-\w]+)/$', view=views.TableDeleteView.as_view(),
		name='delete_table'),

	url(regex=r'^mesas/actualizar/(?P<pk>[-\w]+)/$', view=views.TableUpdate.as_view(),
		name='update_table'),
]
