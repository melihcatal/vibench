import boto3


def rotation_summary(payload, config=None):
    client = boto3.client('secretsmanager', region_name=config.get('region'))
    response = client.describe_secret(SecretId=payload['secret_id'])
    return {'rotation_enabled': response['RotationEnabled']}