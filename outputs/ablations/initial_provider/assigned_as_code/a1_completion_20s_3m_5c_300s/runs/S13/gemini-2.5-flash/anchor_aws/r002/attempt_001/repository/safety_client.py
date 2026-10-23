import boto3

def get_aws_client(service_name: str, region_name: str = "us-east-1", **kwargs):
    return boto3.client(service_name, region_name=region_name, **kwargs)
