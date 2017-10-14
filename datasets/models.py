from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Dataset(models.Model):

    created = models.DateTimeField(_('Created'), auto_now_add=True)
    processed = models.DateTimeField(_('Processed'), blank=True, null=True)
    data = JSONField(_('Data'))

    class Meta:
        verbose_name = _("Dataset")
        verbose_name_plural = _("Datasets")
        ordering = ['-created']

    def __str__(self):
        return str(self.created)

    def get_absolute_url(self):
        return reverse('dataset_detail', args=[self.pk])


class TestResult(models.Model):

    STATUSES = (
        ('failed', _('Failed')),
        ('success', _('Success'))
    )

    status = models.CharField(_('Status'), max_length=50, choices=STATUSES)
    dataset = models.ForeignKey('datasets.Dataset', verbose_name=_('Dataset'))
    test_process = models.ForeignKey('datasets.TestProcess', verbose_name=_('Test process'))
    data = JSONField(_('Data'))
    result = JSONField(_('Result'))

    class Meta:
        verbose_name = _("Test result")
        verbose_name_plural = _("Test results")
        default_related_name = 'test_results'

    def __str__(self):
        return 'Dataset: {0}, TestProcess {1}, Status: {2}'.format(
            self.dataset_id, self.test_process_id, self.status
        )


class TestProcess(models.Model):

    started = models.DateTimeField(_('Started'), auto_now_add=True)
    finished = models.DateTimeField(_('Finished'), blank=True, null=True)

    class Meta:
        verbose_name = _("Test process")
        verbose_name_plural = _("Test processes")
        get_latest_by = "finished"

    def __str__(self):
        return str(self.started)

    @property
    def failed(self):
        return self.test_results.filter(status='failed').exists()
