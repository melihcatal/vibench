import boto3


def summarize_secret_rotation_status(secret_id):
    client = boto3.client("secretsmanager")
    response = client.describe_secret(SecretId=secret_id)
    return response["RotationEnabled"]
