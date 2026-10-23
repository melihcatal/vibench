import boto3


def rotate_secret_version(version_stage="AWSCURRENT"):
    client = boto3.client("secretsmanager")
    secret_name = "ROTATE_SECRET"
    response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
    return response["SecretString"]
