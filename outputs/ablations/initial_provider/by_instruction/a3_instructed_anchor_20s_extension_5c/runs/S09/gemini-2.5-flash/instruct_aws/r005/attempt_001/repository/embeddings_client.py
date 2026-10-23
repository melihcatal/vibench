import boto3
import os

def get_bedrock_client():
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=aws_region
    )

TITAN_EMBED_TEXT_MODEL_ID = "amazon.titan-embed-text-v1"
