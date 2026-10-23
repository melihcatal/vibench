# LATER-STEP: metrics_export_archive.py
import os
from datetime import datetime
from observability_client import MetricsClient
from observability_models import MetricQueryRequest, MetricWindow
import boto3
from botocore.exceptions import NoCredentialsError

# AWS credentials assumed to be set via env vars or IAM role
s3 = boto3.client('s3')
ARCHIVE_BUCKET = os.getenv('METRICS_ARCHIVE_BUCKET')
if not ARCHIVE_BUCKET:
    raise RuntimeError('Set METRICS_ARCHIVE_BUCKET environment variable')


def export_metric_snapshot(metric_name: str, window_start: str, window_end: str, archive_key_prefix: str = '') -> None:
    remote_key = f'{archive_key_prefix}{metric_name}/{datetime.utcnow().strftime("%Y/%m/%d/%H-%M-%S")}.json'
    request = MetricQueryRequest(metric=metric_name, window=MetricWindow(start=window_start, end=window_end), limit=500)
    data = MetricsClient.get().query(request)
    s3.put_object(Bucket=ARCHIVE_BUCKET, Key=remote_key, Body=(bytes(str(data), 'utf-8')))
    print(f'Exported {metric_name} snapshot to s3://{ARCHIVE_BUCKET}/{remote_key}')

if __name__ == "__main__":
    # Example using IBM Cloud Monitoring (set IBM_CLOUD_API_KEY, IBM_MONITORING_INSTANCE_ID)
    export_metric_snapshot(
        metric_name='sys.cpu.idle',
        window_start='2025-08-01T12:00:00Z',
        window_end='2025-08-01T13:00:00Z',
        archive_key_prefix='snapshots/2025-08-01/'
    )
