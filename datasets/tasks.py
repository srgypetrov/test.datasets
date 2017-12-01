import json

from celery import Task, group, task

from .models import Dataset, TestProcess
from .process import test_func, save_result


class TestFuncTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        error = '{0}: {1}'.format(einfo.type.__name__, einfo.exception)
        save_result_task.s(args, {'error': error}).apply_async(queue='third')

    def on_success(self, retval, task_id, args, kwargs):
        save_result_task.s(args, retval).apply_async(queue='third')


@task
def test_datasets_task():
    test_tasks = []
    for dataset in Dataset.objects.not_processed():
        dataset_tasks = []
        for item in dataset.data:
            json_data = json.dumps(item)
            dataset_tasks.append(test_func_task.s(json_data, dataset.pk))
        test_tasks.extend(dataset_tasks)
    TestProcess.objects.create(tests_count=len(test_tasks))
    group(*test_tasks).apply_async(queue='second')


@task(base=TestFuncTask)
def test_func_task(data, dataset_id):
    return test_func(data)


@task
def save_result_task(args, retval):
    save_result(args, retval)
