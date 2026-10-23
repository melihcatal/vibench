import os
import boto3


def get_translation_client(region=None):
    region = region or os.getenv("AWS_REGION")
    return boto3.client("translate", region_name=region)