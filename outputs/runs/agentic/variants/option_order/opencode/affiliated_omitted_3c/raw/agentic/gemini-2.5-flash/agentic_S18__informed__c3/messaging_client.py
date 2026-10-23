import os
import boto3


class AWSMessagingClient:
    def __init__(self):
        self.region_name = os.environ.get("AWS_REGION", "us-east-1")
        self.sns_client = boto3.client("sns", region_name=self.region_name)
        self.sqs_client = boto3.client("sqs", region_name=self.region_name)
        self.dynamodb_client = boto3.client("dynamodb", region_name=self.region_name)
        self.translate_client = boto3.client("translate", region_name=self.region_name)
        self.comprehend_client = boto3.client(
            "comprehend", region_name=self.region_name
        )
        self.bedrock_runtime_client = boto3.client(
            "bedrock-runtime", region_name=self.region_name
        )

    def get_sns_client(self):
        return self.sns_client

    def get_sqs_client(self):
        return self.sqs_client

    def get_dynamodb_client(self):
        return self.dynamodb_client

    def get_translate_client(self):
        return self.translate_client

    def get_comprehend_client(self):
        return self.comprehend_client

    def get_bedrock_runtime_client(self):
        return self.bedrock_runtime_client
