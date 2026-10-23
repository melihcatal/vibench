import boto3

def get_security_client():
    return boto3.client('secretsmanager')