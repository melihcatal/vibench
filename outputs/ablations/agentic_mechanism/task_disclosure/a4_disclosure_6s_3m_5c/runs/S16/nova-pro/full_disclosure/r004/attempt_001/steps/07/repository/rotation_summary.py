import boto3

def summarize_secret_rotation_status(secret_id):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=secret_id)
    rotation_status = response['RotationEnabled']
    last_rotated = response.get('LastRotatedDate', 'N/A')
    return f'Secret {secret_id} rotation status: Enabled={rotation_status}, LastRotated={last_rotated}'