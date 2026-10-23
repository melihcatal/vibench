import boto3


def get_dynamodb_client():
    return boto3.client("dynamodb")
