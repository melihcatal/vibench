import boto3

def get_secretsmanager_client():
    return boto3.client('secretsmanager')

def normalize_secret_response(response):
    return response['SecretString']