from boto3 import client as boto3_client


def record_export_archive(payload, config=None):
    config = config or {}
    s3 = boto3_client('s3', aws_access_key_id=config.get('aws_access_key_id'), aws_secret_access_key=config.get('aws_secret_access_key'), region_name=config.get('region'))
    bucket = config['bucket']
    key = payload['key']
    body = payload['body']
    s3.put_object(Bucket=bucket, Key=key, Body=body)
    return {'bucket': bucket, 'key': key}
