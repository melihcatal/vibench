import boto3

from security_client import load_secret_config
from security_models import select_secret_value


def rotate_secret_version(payload, config=None):
    cfg = load_secret_config(config)
    client = boto3.client("secretsmanager", region_name=cfg["region"])
    params = {"SecretId": payload["secret_id"]}
    if payload.get("version_stage"):
        params["VersionStage"] = payload["version_stage"]
    if payload.get("version_id"):
        params["VersionId"] = payload["version_id"]
    response = client.get_secret_value(**params)
    return {"secret_value": select_secret_value(response)}
