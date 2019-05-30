from django.conf.urls import url

from . import views

app_name = 'users'

urlpatterns = [
    url(regex=r'^registro/$', view=views.SignupView.as_view(),
        name='signup'),

    url(regex=r'^perfil/$', view=views.ProfileView.as_view(),
        name='profile'),

    url(regex=r'^logout/$', view=views.logout_view,
        name='logout'),

    url(regex=r'^login/$', view=views.LoginView.as_view(),
        name='login'),
]
