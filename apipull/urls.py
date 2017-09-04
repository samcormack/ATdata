from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.call_log,name='call_log')
]
