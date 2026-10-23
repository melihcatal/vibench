import boto3


def rotation_summary(secret_id):
    client = boto3.client("secretsmanager")
    response = client.describe_secret(SecretId=secret_id)
    return response["VersionIdsToStages"]
