import os
import boto3
from botocore.config import Config


class StorageClient:
    def __init__(self):
        self.s3_client = self._get_s3_client()

    def _get_s3_client(self):
        # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are typically loaded from environment variables
        # or AWS credentials file by boto3 automatically.
        # Explicitly configuring client with a region
        aws_region = os.getenv(
            "AWS_REGION", "us-east-1"
        )  # Default to us-east-1 if not set
        s3_config = Config(region_name=aws_region)
        return boto3.client("s3", config=s3_config)

    def get_client(self):
        return self.s3_client


class TextractClient:
    def __init__(self):
        self.textract_client = self._get_textract_client()

    def _get_textract_client(self):
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        textract_config = Config(region_name=aws_region)
        return boto3.client("textract", config=textract_config)

    def get_client(self):
        return self.textract_client


class TranslateClient:
    def __init__(self):
        self.translate_client = self._get_translate_client()

    def _get_translate_client(self):
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        translate_config = Config(region_name=aws_region)
        return boto3.client("translate", config=translate_config)

    def get_client(self):
        return self.translate_client


class BedrockRuntimeClient:
    def __init__(self):
        self.bedrock_runtime_client = self._get_bedrock_runtime_client()

    def _get_bedrock_runtime_client(self):
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        bedrock_config = Config(region_name=aws_region)
        return boto3.client("bedrock-runtime", config=bedrock_config)

    def get_client(self):
        return self.bedrock_runtime_client
