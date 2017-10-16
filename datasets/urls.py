from django.conf.urls import url

from .views import (DatasetDetailView, DatasetView, test_process_init,
                    test_process_status)

urlpatterns = [
    url(r'^$', DatasetView.as_view(), name='datasets'),
    url(r'(?P<pk>\d+)/$', DatasetDetailView.as_view(), name='dataset_detail'),
    url(r'init/$', test_process_init, name='test_process_init'),
    url(r'status/$', test_process_status, name='test_process_status')
]
