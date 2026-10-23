import json

from security_client import access_secret_text, build_secret_manager_client, secret_version_name


def parse_json_secret(payload, config=None):
    config = config or {}
    client = build_secret_manager_client()
    name = secret_version_name(config["project_id"], payload["secret_id"], config.get("version", "latest"))
    value = access_secret_text(client, name)
    return {"json_secret": json.loads(value)}
