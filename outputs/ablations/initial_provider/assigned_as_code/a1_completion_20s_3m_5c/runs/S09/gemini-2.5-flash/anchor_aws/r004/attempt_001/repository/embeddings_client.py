import boto3
import os


class EmbeddingsClient:

    def __init__(self, region_name=None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("bedrock-runtime", region_name=self.region_name)

    def get_client(self):
        return self.client
