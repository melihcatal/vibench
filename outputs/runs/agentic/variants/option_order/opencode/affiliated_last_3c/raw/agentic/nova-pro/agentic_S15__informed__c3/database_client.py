import boto3


def get_dynamodb_client():
    return boto3.client("dynamodb")


def get_s3_client():
    return boto3.client("s3")
