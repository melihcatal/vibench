from security_client import load_security_config, secret_manager_client, secret_name
from security_models import parse_json_payload


def parse_json_secret(payload, config=None):
    config = load_security_config(config)
    client = secret_manager_client()
    name = secret_name(config["project_id"], payload["secret_id"], config.get("version", "latest"))
    response = client.access_secret_version(request={"name": name})
    data = parse_json_payload(response.payload.data)
    if payload.get("key_field"):
        return {"secret_value": data[payload["key_field"]]}
    return {"secret_value": data}
