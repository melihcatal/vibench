import os
import boto3


def get_aws_credentials():
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": os.getenv("AWS_REGION", "us-west-2"),
    }


def create_cw_client():
    credentials = get_aws_credentials()
    return boto3.client("cloudwatch", **credentials)
