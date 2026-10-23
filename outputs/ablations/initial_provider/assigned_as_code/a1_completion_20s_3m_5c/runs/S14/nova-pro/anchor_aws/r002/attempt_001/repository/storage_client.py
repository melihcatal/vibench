import boto3


def get_s3_client():
    return boto3.client('s3', region_name='your-region')