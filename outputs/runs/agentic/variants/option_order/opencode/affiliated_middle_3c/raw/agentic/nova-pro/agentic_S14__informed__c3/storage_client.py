import boto3


def get_s3_client():
    return boto3.client("s3")


def get_bucket_name():
    return "your-bucket-name"
