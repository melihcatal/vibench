import boto3


def get_bedrock_client(region_name="us-west-2"):
    return boto3.client("bedrock-runtime", region_name=region_name)
