import boto3


def select_platform_resource():
    client = boto3.client("bedrock")
    model_id = "amazon.titan-text-express-v1"
    return model_id
