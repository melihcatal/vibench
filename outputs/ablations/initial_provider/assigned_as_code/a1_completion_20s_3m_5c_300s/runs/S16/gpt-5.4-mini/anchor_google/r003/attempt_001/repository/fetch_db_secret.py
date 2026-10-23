from google.cloud import secretmanager

from security_client import load_config, secret_name, decode_payload, get_client


def fetch_db_secret(payload, config=None):
    config = load_config(config)
    client = get_client()
    name = secret_name(config["project_id"], payload["secret_id"], config["version"])
    response = client.access_secret_version(request={"name": name})
    return {"db_secret": decode_payload(response)}
