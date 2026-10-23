import boto3


def metrics_export_archive(payload, config=None):
    config = config or {}
    client = boto3.client('s3', region_name=config.get('region', 'us-east-1'))
    client.upload_file(payload['file_path'], config['bucket_name'], payload['object_key'])
    return {'status': 'success'}