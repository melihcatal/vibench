import boto3


def rotate_secret_version(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))

    secret_id = payload["secret_id"]
    version_id = payload.get("version_id")
    version_stage = payload.get("version_stage", "AWSCURRENT")

    if version_id:
        response = client.get_secret_value(SecretId=secret_id, VersionId=version_id)
    else:
        response = client.get_secret_value(SecretId=secret_id, VersionStage=[version_stage])

    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    return {"secret_value": value, "version_id": response.get("VersionId"), "version_stages": response.get("VersionStages")}
