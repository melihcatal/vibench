from security_client import secrets_manager_client, normalize_secret_value


def rotate_secret_version(payload, config=None):
    client = secrets_manager_client(config)
    params = {"SecretId": payload["secret_id"]}
    if payload.get("version_id"):
        params["VersionId"] = payload["version_id"]
    if payload.get("version_stage"):
        params["VersionStage"] = payload["version_stage"]
    response = client.get_secret_value(**params)
    return {"secret_version": normalize_secret_value(response)}
