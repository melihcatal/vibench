import os
import boto3


class ModelClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelClient, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance

    def _initialize_client(self):
        self.bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.bedrock = boto3.client(
            service_name="bedrock",
            region_name=os.environ.get("AWS_REGION", "us-east-1"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )

    def get_bedrock_runtime_client(self):
        return self.bedrock_runtime

    def get_bedrock_client(self):
        return self.bedrock
