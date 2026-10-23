import boto3


def get_dynamodb_client():
    return boto3.resource("dynamodb", region_name="us-west-2")


def get_s3_client():
    return boto3.client("s3")
