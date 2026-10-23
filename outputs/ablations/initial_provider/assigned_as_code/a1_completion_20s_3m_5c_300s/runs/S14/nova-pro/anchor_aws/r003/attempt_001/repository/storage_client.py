import boto3


def get_s3_client(region):
    return boto3.client('s3', region_name=region)


def get_config(bucket):
    return {'bucket': bucket}