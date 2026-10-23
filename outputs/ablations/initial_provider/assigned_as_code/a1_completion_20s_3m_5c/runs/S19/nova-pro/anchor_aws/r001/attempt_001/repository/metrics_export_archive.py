import boto3


def metrics_export_archive(payload, config=None):
    config = config or {}
    client = boto3.client('s3', region_name=config.get('region'))
    client.put_object(Bucket=config['bucket'], Key=payload['key'], Body=payload['data'])
    return {'status': 'success'}