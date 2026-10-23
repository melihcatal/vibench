import os
import boto3


def metrics_export_archive(bucket: str, key: str, data: bytes) -> str:
    client = boto3.client('s3', region_name=os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION') or 'us-east-1')
    client.put_object(Bucket=bucket, Key=key, Body=data)
    return f's3://{bucket}/{key}'
