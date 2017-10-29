from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index, name ='home'),     # This line has changed!
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^success$',views.success)
    ]
