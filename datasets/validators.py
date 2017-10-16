from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def array_only(value):
    if not isinstance(value, list):
        raise ValidationError(_('Dataset must be JSON array.'))
