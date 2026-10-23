import boto3

def archive_metric_snapshot(bucket_name: str, object_key: str, data: bytes):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=object_key, Body=data)

def metrics_export_archive(bucket_name: str, object_key: str, data: bytes):
    archive_metric_snapshot(bucket_name, object_key, data)