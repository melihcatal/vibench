import os, json, boto3
from observability_client import CloudWatchClient
from observability_models import MetricQueryRequest

# AWS S3 configuration via environment variables
AWS_BUCKET = os.getenv('S3_BUCKET')
AWS_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
s3_client = boto3.client('s3', region_name=AWS_REGION)

def metrics_export_archive(metric_name: str, start_time: str, end_time: str, query: MetricQueryRequest, archive_key: str):
    """Archive exported metric snapshots in Amazon S3 managed object storage.

    Pulls metric datapoints, serializes to JSON, and stores in S3.
    """
    client = CloudWatchClient(region=AWS_REGION)
    datapoints = client.get_metric_data(query)
    payload = json.dumps(datapoints, indent=2)
    s3_client.put_object(Bucket=AWS_BUCKET, Key=archive_key, Body=payload)
