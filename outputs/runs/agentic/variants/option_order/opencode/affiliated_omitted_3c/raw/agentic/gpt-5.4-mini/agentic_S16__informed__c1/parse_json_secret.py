from security_client import (
    fetch_secret_value,
    load_secret_config,
    secrets_manager_client,
)
from security_models import parse_json_secret as parse_json_secret_payload


def parse_json_secret(secret_id: str):
    config = load_secret_config(secret_id=secret_id)
    client = secrets_manager_client(config.region_name)
    response = fetch_secret_value(client, config)
    return parse_json_secret_payload(secret_id, response).data
