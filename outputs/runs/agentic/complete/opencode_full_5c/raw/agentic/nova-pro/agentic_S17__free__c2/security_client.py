import os
import boto3


def get_kms_client():
    return boto3.client("kms", region_name=os.getenv("AWS_REGION", "us-west-2"))
