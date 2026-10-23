import boto3


def select_resource():
    bedrock = boto3.client("bedrock")
    response = bedrock.list_foundation_models()
    return response
