import boto3


def summarize_rotation_status():
    client = boto3.client("secretsmanager")
    response = client.describe_secret(SecretId="rotation-secret")
    return response["RotationEnabled"]
