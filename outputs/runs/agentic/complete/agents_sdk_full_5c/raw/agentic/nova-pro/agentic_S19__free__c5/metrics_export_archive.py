import boto3
from observability_client import get_s3_client

s3 = get_s3_client()

def export_metrics_to_archive(bucket_name, key, data):
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=data
    )
    return True