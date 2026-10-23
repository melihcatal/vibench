import os
import boto3


def get_cw_logs_client():
    region_name = os.getenv("AWS_REGION", "us-west-2")
    return boto3.client("logs", region_name=region_name)
