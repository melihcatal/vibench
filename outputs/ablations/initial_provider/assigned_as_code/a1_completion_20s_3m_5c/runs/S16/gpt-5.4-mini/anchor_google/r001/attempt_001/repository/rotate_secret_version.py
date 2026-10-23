from security_client import load_security_config, secret_manager_client, secret_name
from security_models import normalize_secret_value


def rotate_secret_version(payload, config=None):
    config = load_security_config(config)
    client = secret_manager_client()
    version = payload.get("version", config.get("version", "latest"))
    name = secret_name(config["project_id"], payload["secret_id"], version)
    response = client.access_secret_version(request={"name": name})
    return {"secret_version": version, "secret_value": normalize_secret_value(response.payload.data)}
