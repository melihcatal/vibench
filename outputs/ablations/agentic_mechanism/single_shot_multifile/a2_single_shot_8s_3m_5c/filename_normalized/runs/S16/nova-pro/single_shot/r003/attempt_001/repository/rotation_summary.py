from security_client import get_secrets_client

def get_rotation_summary(secret_id):
    client = get_secrets_client()
    response = client.describe_secret(SecretId=secret_id)
    return response['RotationEnabled'], response['RotationLambdaARN']