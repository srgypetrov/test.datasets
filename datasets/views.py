from celery import current_app, states
from celery.result import AsyncResult
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.urlresolvers import reverse
from django.db.models import Case, IntegerField, Sum, When
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from .forms import DatasetModelForm
from .models import Dataset, TestProcess
from .tasks import test_datasets_task


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
        test_process = qs.first()
        return {
            'test_process': test_process,
            'test_process_datasets': set(getattr(test_process, 'datasets', []))
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


def test_process_init(request):
    inspector = current_app.control.inspect()
    active_tasks = inspector.active()
    for worker, tasks in active_tasks.items():
        if tasks:
            return JsonResponse({'error': 'Test process is already running.'})
    if not Dataset.objects.not_processed().exists():
        return JsonResponse({'error': 'No data sets not processed.'})
    task = test_datasets_task.apply_async(queue='first')
    url = '{0}?task_id={1}'.format(reverse('test_process_status'), task.id)
    return JsonResponse({'status_url': url})


def test_process_status(request):
    task_id = request.GET.get('task_id', None)
    if task_id is None:
        return JsonResponse({'error': 'No task id given.'})
    task = AsyncResult(task_id)
    if task.state == states.SUCCESS:
        finished = not TestProcess.objects.processed_now().exists()
    else:
        finished = False
    return JsonResponse({'finished': finished})
