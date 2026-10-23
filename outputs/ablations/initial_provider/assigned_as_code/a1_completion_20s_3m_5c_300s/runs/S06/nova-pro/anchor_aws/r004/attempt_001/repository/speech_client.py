import boto3


def get_polly_client(config):
    region = config.get('region', 'us-west-2')
    return boto3.client('polly', region_name=region)