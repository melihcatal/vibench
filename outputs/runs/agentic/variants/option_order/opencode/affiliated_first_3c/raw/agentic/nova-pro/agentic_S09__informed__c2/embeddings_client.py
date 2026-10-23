import boto3


def embeddings_client():
    return boto3.client("bedrock-runtime")
