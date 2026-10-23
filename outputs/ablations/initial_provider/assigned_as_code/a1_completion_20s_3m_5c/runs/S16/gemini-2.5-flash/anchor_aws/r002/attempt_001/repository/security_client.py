import boto3

def get_secrets_manager_client(region_name=None):
    return boto3.client("secretsmanager", region_name=region_name)
