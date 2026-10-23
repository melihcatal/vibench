import boto3

client = boto3.client('secretsmanager')

def rotation_summary(secret_name):
    response = client.describe_secret(SecretId=secret_name)
    return response['RotationEnabled']