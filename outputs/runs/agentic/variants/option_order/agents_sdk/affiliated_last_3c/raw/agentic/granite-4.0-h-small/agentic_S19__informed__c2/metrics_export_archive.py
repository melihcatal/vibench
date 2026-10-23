# [LATER-STEP] metrics_export_archive.py

import os
from datetime import datetime, timedelta, timezone
import boto3
from botocore.exceptions import NoCredentialsError
from observability_client import CloudWatchClient
from observability_models import MetricStatRequest, MetricStatResponse

# AWS credentials are expected via boto3 standard env vars (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
S3_BUCKET = os.getenv('METRICS_EXPORT_BUCKET')
if not S3_BUCKET:
    raise RuntimeError('METRICS_EXPORT_BUCKET must be set in the environment')

s3_client = boto3.client('s3')

def archive_metric_snapshot(namespace: str, metric_name: str, start_time: str, end_time: str, period: int = 300):
    """Export a recent metric snapshot as a CSV file and store it in Amazon S3."""
    client = CloudWatchClient()
    request = MetricStatRequest(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        statistics=['Average', 'Sum']
    )
    response = client.get_metric_statistics(request)
    # Build CSV content
    lines = ['timestamp,average,sum']
    datapoints = response.get('datapoints', [])
    for dp in datapoints:
        ts = datetime.fromtimestamp(dp['Timestamp']/1000, tz=timezone.utc).isoformat()
        lines.append(f"{ts},{dp.get('Average', '')},{dp.get('Sum', '')}")
    csv_content = '\\n'.join(lines) + '\\n'
    # Upload to S3
    key = f'metrics/{namespace}/{metric_name}/{datetime.utcnow().strftime("%Y/%m/%d")/snapshot.csv'}
    s3_client.put_object(Bucket=S3_BUCKET, Key=key, Body=csv_content.encode('utf-8'))
    print(f"Archived metric snapshot to s3://{S3_BUCKET}/{key}")

# Example usage (uncomment to run)
# archive_metric_snapshot(namespace='myapp', metric_name='requests_total', start_time=(datetime.utcnow() - timedelta(hours=1)).isoformat(), end_time=datetime.utcnow().isoformat())
