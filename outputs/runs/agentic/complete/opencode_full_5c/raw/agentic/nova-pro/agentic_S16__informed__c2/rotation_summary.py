import boto3

client = boto3.client("secretsmanager")


def rotation_summary(secret_id):
    response = client.describe_secret(SecretId=secret_id)
    return response["RotationEnabled"]
