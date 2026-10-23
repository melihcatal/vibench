import boto3


def summarize_rotation_status(secret_name):
    client = boto3.client("secretsmanager")
    response = client.describe_secret(SecretId=secret_name)
    return response["VersionIdsToStages"]
