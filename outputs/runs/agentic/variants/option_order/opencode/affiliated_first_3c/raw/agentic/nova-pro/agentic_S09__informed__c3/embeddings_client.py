import boto3


def create_embeddings_client():
    return boto3.client("bedrock-runtime")
