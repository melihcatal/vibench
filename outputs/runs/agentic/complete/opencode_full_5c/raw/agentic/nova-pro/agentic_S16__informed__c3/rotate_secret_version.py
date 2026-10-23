import boto3


def rotate_secret_version(secret_name, version_stage):
    client = boto3.client("secretsmanager")
    describe_secret_response = client.describe_secret(SecretId=secret_name)
    for version in describe_secret_response["VersionIdsToStages"]:
        if version_stage in describe_secret_response["VersionIdsToStages"][version]:
            return version
    return None
