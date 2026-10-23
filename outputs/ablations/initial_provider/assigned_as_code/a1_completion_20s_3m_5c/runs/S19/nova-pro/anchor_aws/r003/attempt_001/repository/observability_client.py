import os

import boto3

def get_config():
    return {
        "region": os.getenv("AWS_REGION", "us-west-2"),
        "namespace": os.getenv("CLOUDWATCH_NAMESPACE", "MyAppMetrics"),
    }

def create_cloudwatch_client():
    config = get_config()
    return boto3.client("cloudwatch", region_name=config["region"])