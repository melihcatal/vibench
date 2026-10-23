import boto3
import os

class MessagingClient:
    def __init__(self):
        self.sns_client = boto3.client(
            "sns",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )

    def get_sns_client(self):
        return self.sns_client
