import boto3


def rotate_secret_version(secret_name, version_stage="AWSCURRENT"):
    client = boto3.client("secretsmanager", region_name="us-west-2")
    response = client.describe_secret(SecretId=secret_name)
    versions = response["VersionIdsToStages"]
    version_id = next(k for k, v in versions.items() if version_stage in v)
    version_response = client.get_secret_value(
        SecretId=secret_name, VersionId=version_id
    )
    return version_response["SecretString"]
