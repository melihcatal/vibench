import boto3


def summarize_secret_rotation(payload):
    client = boto3.client('secretsmanager')
    response = client.describe_secret(SecretId=payload['secret_id'])
    rotation_status = response['RotationEnabled']
    return {'rotation_status': rotation_status}