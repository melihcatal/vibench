import boto3

from security_client import load_config, normalize_secret_value, secret_identifier


def rotate_secret_version(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    request = {"SecretId": secret_identifier(payload)}
    if payload.get("version_id"):
        request["VersionId"] = payload["version_id"]
    if payload.get("version_stage"):
        request["VersionStage"] = payload["version_stage"]
    response = client.get_secret_value(**request)
    return {"secret": normalize_secret_value(response), "version_id": response.get("VersionId"), "version_stages": response.get("VersionStages", [])}
