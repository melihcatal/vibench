import boto3


def get_polly_client(config):
    return boto3.client('polly', region_name=config.get('region'))