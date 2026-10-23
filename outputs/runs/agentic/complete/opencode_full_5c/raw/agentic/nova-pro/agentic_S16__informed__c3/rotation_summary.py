import boto3


def summarize_secret_rotation(secret_name):
    client = boto3.client("secretsmanager")
    describe_secret_response = client.describe_secret(SecretId=secret_name)
    return describe_secret_response["VersionIdsToStages"]
