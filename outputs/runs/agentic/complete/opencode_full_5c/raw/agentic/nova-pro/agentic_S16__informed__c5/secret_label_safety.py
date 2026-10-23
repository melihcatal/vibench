import boto3


def check_secret_labels(secret_id):
    client = boto3.client("secretsmanager")
    response = client.describe_secret(SecretId=secret_id)
    return response["Tags"]
