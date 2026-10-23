import boto3
import os

class SecurityClient:
    def __init__(self):
        self.region_name = os.environ.get("AWS_REGION", "us-east-1")
        self.kms_client = boto3.client("kms", region_name=self.region_name)

    def get_kms_client(self):
        return self.kms_client