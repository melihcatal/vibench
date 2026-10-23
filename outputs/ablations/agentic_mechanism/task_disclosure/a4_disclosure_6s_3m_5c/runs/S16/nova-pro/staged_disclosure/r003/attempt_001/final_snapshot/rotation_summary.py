import boto3

def summarize_secret_rotation_status(secret_name):
    client = boto3.client('secretsmanager')
    try:
        response = client.describe_secret(SecretId=secret_name)
        rotation_status = response.get('RotationEnabled', False)
        return f'Rotation status for secret {secret_name}: {