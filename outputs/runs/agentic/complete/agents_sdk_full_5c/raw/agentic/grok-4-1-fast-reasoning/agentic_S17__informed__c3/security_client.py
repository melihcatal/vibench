import os
import boto3
from botocore.exceptions import ClientError

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

def get_kms_client():
    return boto3.client('kms', region_name=AWS_REGION)