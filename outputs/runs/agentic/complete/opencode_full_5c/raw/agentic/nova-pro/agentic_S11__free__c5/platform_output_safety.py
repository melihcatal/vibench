import boto3

bedrock_client = boto3.client("bedrock-runtime")


def check_safety(output):
    # Placeholder for safety check logic
    return True
