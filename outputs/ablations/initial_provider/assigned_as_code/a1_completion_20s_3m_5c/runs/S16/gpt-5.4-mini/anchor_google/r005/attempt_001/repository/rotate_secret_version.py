import json

from security_client import access_secret_text, build_secret_manager_client, secret_version_name


def rotate_secret_version(payload, config=None):
    config = config or {}
    client = build_secret_manager_client()
    version = payload.get("version") or config.get("version", "latest")
    name = secret_version_name(config["project_id"], payload["secret_id"], version)
    value = access_secret_text(client, name)
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        parsed = {"value": value}
    return {"secret_version": version, "secret": parsed}
