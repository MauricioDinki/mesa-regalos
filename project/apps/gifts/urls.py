from django.conf.urls import url

from . import views

app_name = 'gifts'

urlpatterns = [
    url(regex=r'^regalos/$', view=views.GiftsTableView.as_view(),
        name='gifts'),

    url(regex=r'^regalos/$', view=views.GiftsTableView.as_view(),
        name='gifts'),

    url(regex=r'^mesas/actualizar/(?P<pk>[-\w]+)/regalos/$',
        view=views.UpdateGiftsTableView.as_view(),
        name='update_gifts'),
]
