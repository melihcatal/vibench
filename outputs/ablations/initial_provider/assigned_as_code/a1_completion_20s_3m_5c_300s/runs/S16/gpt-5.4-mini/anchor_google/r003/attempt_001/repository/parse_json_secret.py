from google.cloud import secretmanager

from security_client import load_config, secret_name, decode_payload, get_client
from security_models import parse_json_secret as parse_secret


def parse_json_secret(payload, config=None):
    config = load_config(config)
    client = get_client()
    name = secret_name(config["project_id"], payload["secret_id"], config["version"])
    response = client.access_secret_version(request={"name": name})
    data = parse_secret(decode_payload(response))
    if payload.get("key_field"):
        data = data[payload["key_field"]]
    return {"secret": data}
