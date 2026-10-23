import boto3


def record_export_archive(payload, config=None):
    config = config or {}
    s3 = boto3.client('s3', region_name=config.get('region'))
    key = payload['key']
    s3.put_object(Bucket=config['bucket'], Key=key, Body=payload['content'])
    return {'archive_key': key}
