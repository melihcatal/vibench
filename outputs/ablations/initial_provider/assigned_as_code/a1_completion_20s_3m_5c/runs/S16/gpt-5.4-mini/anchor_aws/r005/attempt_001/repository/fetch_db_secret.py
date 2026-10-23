import boto3

from security_client import load_config, secret_string
from security_models import parse_json_secret, select_field


def fetch_db_secret(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    request = {"SecretId": payload["secret_id"]}
    if payload.get("version_stage") or config.get("version_stage"):
        request["VersionStage"] = payload.get("version_stage") or config.get("version_stage")
    if payload.get("version_id") or config.get("version_id"):
        request["VersionId"] = payload.get("version_id") or config.get("version_id")
    response = client.get_secret_value(**request)
    secret = parse_json_secret(secret_string(response))
    return {"db_secret": select_field(secret, payload.get("field"))}
