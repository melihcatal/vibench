from google.cloud import secretmanager

from security_client import load_config, secret_name, get_client


def rotation_summary(payload, config=None):
    config = load_config(config)
    client = get_client()
    name = secret_name(config["project_id"], payload["secret_id"], payload.get("version", config["version"]))
    response = client.access_secret_version(request={"name": name})
    return {"status": "available", "secret_name": name, "payload_size": len(response.payload.data)}
