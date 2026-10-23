import boto3


def rotate_secret_version(secret_id, version_id):
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id, VersionId=version_id)
    return response["SecretString"]
