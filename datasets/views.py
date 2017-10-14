from django.db.models import Case, IntegerField, Sum, When
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .forms import DatasetModelForm
from .models import Dataset, TestProcess


class DatasetView(ListView, FormMixin):

    paginate_by = 6
    form_class = DatasetModelForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test_process'] = self.get_last_test_process()
        return context

    def get_last_test_process(self):
        try:
            return TestProcess.objects.filter(finished__isnull=False).latest()
        except TestProcess.DoesNotExist:
            return None

    def get_queryset(self):
        return Dataset.objects.annotate(
            failed_results=Sum(
                Case(
                    When(testresult__status='failed', then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
