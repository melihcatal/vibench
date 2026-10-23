import boto3


def get_storage_client():
    return boto3.client("s3")
