import boto3


def rotate_secret_version(secret_name, version_stage):
    client = boto3.client("secretsmanager")
    response = client.describe_secret(SecretId=secret_name)
    versions = response["VersionIdsToStages"]
    for version_id, stages in versions.items():
        if version_stage in stages:
            return version_id
    return None
