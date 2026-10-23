import boto3
from observability_client import create_cw_client

s3_client = boto3.client("s3")


def metrics_export_archive(bucket_name, key, data):
    s3_client.put_object(Bucket=bucket_name, Key=key, Body=data)
