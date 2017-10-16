from celery.result import AsyncResult
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Case, IntegerField, Sum, When
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import DatasetModelForm
from .models import Dataset, TestProcess
from .tasks import test_datasets


class DatasetView(ListView, FormMixin):

    paginate_by = 6
    form_class = DatasetModelForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect('datasets')
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_process_data = self.get_test_process_data()
        context.update(test_process_data)
        return context

    def get_test_process_data(self):
        qs = TestProcess.objects.processed()
        qs = qs.annotate(datasets=ArrayAgg('test_results__dataset_id'))
        test_process = qs.last()
        return {
            'test_process': test_process,
            'test_process_datasets': set(test_process.datasets)
        }

    def get_queryset(self):
        return Dataset.objects.annotate(
            failed_results=Sum(
                Case(
                    When(testresult__status='failed', then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).prefetch_related('test_results')


class DatasetDetailView(DetailView):

    model = Dataset
