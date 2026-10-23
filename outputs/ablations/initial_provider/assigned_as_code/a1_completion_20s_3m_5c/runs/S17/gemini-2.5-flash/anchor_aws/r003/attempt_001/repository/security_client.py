import boto3

def get_kms_client(region_name=None):
    return boto3.client("kms", region_name=region_name)
