from django import forms
from django.contrib.postgres.forms import JSONField as BaseJSONField
from django.utils.translation import ugettext_lazy as _

from .models import Dataset


class JSONField(BaseJSONField):

    def prepare_value(self, value):
        if value is None:
            return None
        return super().prepare_value(value)


class DatasetModelForm(forms.ModelForm):

    data = JSONField(
        error_messages={'required': _('Dataset can not be empty.')},
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3}
        )
    )

    class Meta:
        model = Dataset
        fields = ['data']
