import boto3
import os

class AWSPollyClient:
    """
    Provides a configured AWS Polly client.
    """
    def __init__(self):
        self.client = boto3.client(
            "polly",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
        )

    def get_client(self):
        return self.client
