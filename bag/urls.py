from django.conf.urls import url

from . import views

app_name = 'bag'

urlpatterns = [
    url(r'^upload/$', views.FileUploadView.as_view())
]