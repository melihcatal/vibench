import boto3


def select_platform_resource():
    client = boto3.client("bedrock")
    response = client.list_foundation_models()
    return response
