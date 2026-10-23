import boto3

def get_comprehend_client(region_name: str = "us-east-1"):
    return boto3.client("comprehend", region_name=region_name)
