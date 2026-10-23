from security_client import get_secrets_manager_client, get_default_stage
from security_models import secret_text, parse_json_secret_value


def rotate_secret_version(payload, config=None):
    client = get_secrets_manager_client(config)
    kwargs = {"SecretId": payload["secret_id"]}
    if payload.get("version_id"):
        kwargs["VersionId"] = payload["version_id"]
    else:
        kwargs["VersionStage"] = payload.get("version_stage") or get_default_stage(config)
    response = client.get_secret_value(**kwargs)
    value = secret_text(response)
    if payload.get("parse_json"):
        value = parse_json_secret_value(value)
    return {"secret_version": value, "version_id": response.get("VersionId"), "version_stages": response.get("VersionStages", [])}
