import boto3

def embed_secret_audit_notes(secret_name):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_name)
    return ' '.join(response['Tags'].keys())