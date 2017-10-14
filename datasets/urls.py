from django.conf.urls import url

from .views import DatasetView


urlpatterns = [
    url(r'^$', DatasetView.as_view(), name='datasets'),
]
