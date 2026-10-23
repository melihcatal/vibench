import boto3


def rotate_secret_version(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(
        SecretId=payload["secret_id"],
        VersionId=payload.get("version_id"),
        VersionStage=payload.get("version_stage", "AWSCURRENT"),
    )
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"]
    return {"secret_value": value}
