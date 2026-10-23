import boto3


def get_s3_client(config):
    return boto3.client('s3', region_name=config.get('region', 'us-west-2'))