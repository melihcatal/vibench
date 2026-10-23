import boto3


def summarize_secret_rotation():
    client = boto3.client("secretsmanager")
    secret_name = "ROTATE_SECRET"
    response = client.describe_secret(SecretId=secret_name)
    return response["RotationEnabled"]
