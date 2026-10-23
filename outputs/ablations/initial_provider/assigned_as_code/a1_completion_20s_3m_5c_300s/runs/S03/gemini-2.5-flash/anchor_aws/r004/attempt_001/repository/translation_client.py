import boto3

def get_translate_client(region: str = "us-east-1"):
    return boto3.client("translate", region_name=region)
