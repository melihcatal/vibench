import boto3
import os


class KmsClient:
    def __init__(self):
        # AWS Key Management Service client
        self.client = boto3.client(
            "kms", region_name=os.getenv("AWS_REGION", "us-east-1")
        )

    def get_client(self):
        return self.client
