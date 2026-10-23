import os
import boto3


def get_aws_credentials():
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    return AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def create_comprehend_client():
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY = get_aws_credentials()
    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
    )
    return comprehend
