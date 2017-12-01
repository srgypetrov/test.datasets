from django.contrib import admin

from .models import Dataset, TestProcess, TestResult


class TestResultInline(admin.StackedInline):

    model = TestResult
    readonly_fields = ['data', 'result', 'status', 'created', 'dataset']

    def has_add_permission(self, request):
        return False


class TestProcessAdmin(admin.ModelAdmin):

    inlines = [TestResultInline]

    def has_add_permission(self, request):
        return False


admin.site.register(Dataset)
admin.site.register(TestProcess, TestProcessAdmin)
