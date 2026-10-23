import boto3


def image_asset_archive(payload, config=None):
    s3 = boto3.client('s3', region_name=config['region'], aws_access_key_id=config['aws_access_key_id'], aws_secret_access_key=config['aws_secret_access_key'])
    s3.put_object(Bucket=config['bucket_name'], Key=payload['image_name'], Body=payload['image_bytes'])
    return {'archived': True}