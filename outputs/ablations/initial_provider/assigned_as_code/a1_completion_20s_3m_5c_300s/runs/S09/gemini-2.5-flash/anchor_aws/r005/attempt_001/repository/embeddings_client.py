import boto3
import os

class BedrockEmbeddingsClient:
    def __init__(self, region_name=None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("bedrock-runtime", region_name=self.region_name)
        self.model_id = "amazon.titan-embed-text-v2:0"

    def get_client(self):
        return self.client

    def get_model_id(self):
        return self.model_id
