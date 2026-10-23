from security_client import load_security_config, secret_manager_client, secret_name
from security_models import normalize_secret_value


def fetch_db_secret(payload, config=None):
    config = load_security_config(config)
    client = secret_manager_client()
    name = secret_name(config["project_id"], payload["secret_id"], config.get("version", "latest"))
    response = client.access_secret_version(request={"name": name})
    value = normalize_secret_value(response.payload.data)
    return {"db_secret": value}
