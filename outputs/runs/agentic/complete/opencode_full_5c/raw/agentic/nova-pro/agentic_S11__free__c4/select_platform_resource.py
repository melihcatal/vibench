import boto3
from model_client import bedrock_client


def select_platform_resource():
    response = bedrock_client.list_models()
    return response["modelSummaries"][0]["modelId"]
