import os
import boto3


def get_kms_client():
    return boto3.client("kms", region_name=os.environ.get("AWS_REGION", "us-east-1"))


def get_cloudtrail_client():
    return boto3.client(
        "cloudtrail", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )


AWS_KMS_KEY_ID = os.environ.get("AWS_KMS_KEY_ID")
