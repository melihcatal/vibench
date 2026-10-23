import os
import boto3


def metrics_export_archive(payload, config=None):
    config = dict(config or {})
    bucket = config.get('bucket') or os.environ['AWS_S3_BUCKET']
    key = payload['key']
    body = payload['content'].encode('utf-8') if isinstance(payload.get('content', ''), str) else payload.get('content', b'')
    client = boto3.client('s3')
    client.put_object(Bucket=bucket, Key=key, Body=body)
    return {'bucket': bucket, 'key': key}
