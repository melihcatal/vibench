import boto3

from vision_client import load_vision_config


def image_asset_archive(payload, config=None):
    cfg = load_vision_config(config)
    s3 = boto3.client('s3')
    bucket = cfg['container_name']
    key = payload['key']
    data = payload.get('data', b'')
    s3.put_object(Bucket=bucket, Key=key, Body=data)
    return {'archived': True, 'bucket': bucket, 'key': key}
