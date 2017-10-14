from django.conf.urls import url

from .views import DatasetView, DatasetDetailView


urlpatterns = [
    url(r'^$', DatasetView.as_view(), name='datasets'),
    url(r'(?P<pk>\d+)/$', DatasetDetailView.as_view(), name='dataset_detail'),
]
