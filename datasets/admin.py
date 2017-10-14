from django.contrib import admin

from .models import Dataset, TestProcess, TestResult


admin.site.register(Dataset)
admin.site.register(TestProcess)
admin.site.register(TestResult)
