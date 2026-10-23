import boto3

from security_client import load_config, secret_string


def rotate_secret_version(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    request = {"SecretId": payload["secret_id"]}
    if payload.get("version_id") or config.get("version_id"):
        request["VersionId"] = payload.get("version_id") or config.get("version_id")
    if payload.get("version_stage") or config.get("version_stage"):
        request["VersionStage"] = payload.get("version_stage") or config.get("version_stage")
    response = client.get_secret_value(**request)
    return {"version": secret_string(response), "version_id": response.get("VersionId"), "version_stages": response.get("VersionStages", [])}
