import boto3
import os

class DocumentClient:
    def __init__(self, region_name=None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.textract_client = boto3.client("textract", region_name=self.region_name)
        self.translate_client = boto3.client("translate", region_name=self.region_name)
        self.comprehend_client = boto3.client("comprehend", region_name=self.region_name)
        self.bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=self.region_name)
        self.s3_client = boto3.client("s3", region_name=self.region_name) # Added for S3 operations if needed
