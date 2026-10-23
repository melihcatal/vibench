import os
from boto3 import client


def metrics_export_archive(bucket, key, body, content_type='application/json'):
    s3 = client('s3')
    s3.put_object(Bucket=bucket, Key=key, Body=body if isinstance(body, (bytes, bytearray)) else str(body).encode(), ContentType=content_type)
    return {'bucket': bucket, 'key': key, 'archived': True, 'service': 'amazon-s3'}
