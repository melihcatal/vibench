import boto3


def get_polly_client(region_name=None):
    return boto3.client("polly", region_name=region_name)