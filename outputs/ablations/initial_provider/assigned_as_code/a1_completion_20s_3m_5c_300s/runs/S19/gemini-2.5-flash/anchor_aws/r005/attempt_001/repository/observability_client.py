import boto3


def get_cloudwatch_client(region_name):
    return boto3.client("cloudwatch", region_name=region_name)
