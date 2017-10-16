import json

from .models import TestResult, TestProcess


def test_func(data):
    d = json.loads(data)
    return {'result': d['a'] + d['b']}


def save_result(args, retval):
    data, dataset_id = args
    status = 'failed' if 'error' in retval else 'success'
    test_process = TestProcess.objects.processed_now().last()
    TestResult.objects.create(
        status=status,
        data=json.loads(data),
        result=retval,
        dataset_id=dataset_id,
        test_process_id=test_process.pk
    )
