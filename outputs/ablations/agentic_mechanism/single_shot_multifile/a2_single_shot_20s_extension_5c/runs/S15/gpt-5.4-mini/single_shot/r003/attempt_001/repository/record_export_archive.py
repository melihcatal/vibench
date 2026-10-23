import os
import boto3

_s3 = boto3.client('s3')


def handler(event, context=None):
    bucket = os.environ['ARCHIVE_BUCKET_NAME']
    key = event.get('key', 'export.json') if isinstance(event, dict) else 'export.json'
    body = event.get('body', '') if isinstance(event, dict) else ''
    _s3.put_object(Bucket=bucket, Key=key, Body=body.encode('utf-8') if isinstance(body, str) else body)
    return {'bucket': bucket, 'key': key, 'archived': True}
