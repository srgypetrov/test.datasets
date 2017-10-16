from django.db.models import QuerySet, Count, F


class DatasetQuerySet(QuerySet):

    def processed(self):
        qs = self.annotate(result_count=Count('test_results'))
        return qs.filter(result_count=F('tests_count'))

    def not_processed(self):
        qs = self.annotate(result_count=Count('test_results'))
        return qs.filter(result_count=0)


class TestProcessQuerySet(DatasetQuerySet):

    def processed_now(self):
        qs = self.annotate(result_count=Count('test_results'))
        return qs.exclude(result_count=F('tests_count'))
