import os
import boto3

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def get_bedrock_client():
    return boto3.client(
        "bedrock-runtime",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def get_model_id(model_family):
    if model_family == "amazon.titan":
        return "amazon.titan-text-express-v1"
    elif model_family == "anthropic":
        return "anthropic.claude-v2"
    else:
        raise ValueError("Unsupported model family")
