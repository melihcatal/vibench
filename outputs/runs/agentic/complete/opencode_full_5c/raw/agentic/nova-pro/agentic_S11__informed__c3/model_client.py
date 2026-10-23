import os
import boto3

AWS_REGION = os.getenv("AWS_REGION", "us-west-2")


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=AWS_REGION)


def get_model_id():
    return os.getenv("MODEL_ID", "amazon.titan-text-express-v1")
