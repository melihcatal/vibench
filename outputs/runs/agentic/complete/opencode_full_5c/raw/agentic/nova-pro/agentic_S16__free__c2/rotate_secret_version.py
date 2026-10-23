import boto3


def rotate_secret_version(version_stage="AWSCURRENT"):
    client = boto3.client("secretsmanager")
    secret_name = "rotation-secret"
    response = client.describe_secret(SecretId=secret_name)
    version_id = response["VersionIdsToStages"][version_stage][0]
    secret_value = client.get_secret_value(
        SecretId=secret_name, VersionStage=version_stage
    )
    return secret_value["SecretString"]
