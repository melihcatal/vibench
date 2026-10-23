from google.cloud import secretmanager

from security_client import load_config, secret_name, decode_payload, get_client


def rotate_secret_version(payload, config=None):
    config = load_config(config)
    client = get_client()
    version = payload.get("version") or config["stage"]
    name = secret_name(config["project_id"], payload["secret_id"], version)
    response = client.access_secret_version(request={"name": name})
    return {"rotated_secret": decode_payload(response), "version": version}
