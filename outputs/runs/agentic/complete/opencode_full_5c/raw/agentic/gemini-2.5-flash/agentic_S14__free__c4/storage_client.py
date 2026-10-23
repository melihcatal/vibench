import boto3
from botocore.exceptions import ClientError
import os


class StorageClient:
    def __init__(self):
        self.s3_client = boto3.client("s3")

    def get_s3_client(self):
        return self.s3_client

    def get_textract_client(self):
        return boto3.client(
            "textract", region_name=os.environ.get("AWS_REGION", "us-east-1")
        )

    def get_translate_client(self):
        return boto3.client(
            "translate", region_name=os.environ.get("AWS_REGION", "us-east-1")
        )

    def get_bedrock_runtime_client(self):
        return boto3.client(
            "bedrock-runtime", region_name=os.environ.get("AWS_REGION", "us-east-1")
        )
