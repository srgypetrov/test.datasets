from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .querysets import DatasetQuerySet, TestProcessQuerySet
from .validators import array_only


class BaseTestModel(models.Model):

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    tests_count = models.IntegerField(_('Tests count'), blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.created)

    @property
    def failed(self):
        return self.test_results.filter(status='failed').exists()

    @property
    def processed(self):
        return self.test_results.count() == self.tests_count

    @property
    def processed_at(self):
        test_result = self.test_results.first()
        return getattr(test_result, 'created', None)


class Dataset(BaseTestModel):

    data = JSONField(_('Data'), validators=[array_only])
    objects = DatasetQuerySet.as_manager()

    class Meta:
        verbose_name = _("Dataset")
        verbose_name_plural = _("Datasets")
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse('dataset_detail', args=[self.pk])


class TestResult(models.Model):

    STATUSES = (
        ('failed', _('Failed')),
        ('success', _('Success'))
    )

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    status = models.CharField(_('Status'), max_length=50, choices=STATUSES)
    dataset = models.ForeignKey('datasets.Dataset', verbose_name=_('Dataset'))
    test_process = models.ForeignKey('datasets.TestProcess', verbose_name=_('Test process'))
    data = JSONField(_('Data'))
    result = JSONField(_('Result'))

    class Meta:
        verbose_name = _("Test result")
        verbose_name_plural = _("Test results")
        default_related_name = 'test_results'
        ordering = ['-created']

    def __str__(self):
        return 'Dataset: {0}, TestProcess {1}, Status: {2}'.format(
            self.dataset_id, self.test_process_id, self.status
        )


class TestProcess(BaseTestModel):

    objects = TestProcessQuerySet.as_manager()

    class Meta:
        verbose_name = _("Test process")
        verbose_name_plural = _("Test processes")
        ordering = ['-created']
