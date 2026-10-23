import os
from observability_client import get_s3_client


def archive_metric_snapshot(bucket_name: str, object_key: str, data: str):
    client = get_s3_client()

    response = client.put_object(Bucket=bucket_name, Key=object_key, Body=data)
    return response
