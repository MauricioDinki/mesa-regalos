from django.conf.urls import url

from . import views

app_name = 'info'

urlpatterns = [
    url(regex=r'^$', view=views.HomeView.as_view(),
        name='home'),
]
