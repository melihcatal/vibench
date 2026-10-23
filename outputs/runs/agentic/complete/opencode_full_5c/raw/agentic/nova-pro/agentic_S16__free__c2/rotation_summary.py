import boto3


def summarize_secret_rotation_status():
    client = boto3.client("secretsmanager")
    secret_name = "example-secret"
    response = client.describe_secret(SecretId=secret_name)
    versions = response["VersionIdsToStages"]
    return versions
