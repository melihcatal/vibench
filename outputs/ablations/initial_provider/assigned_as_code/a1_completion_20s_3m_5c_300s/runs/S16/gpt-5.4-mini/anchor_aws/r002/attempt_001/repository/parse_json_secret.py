from security_client import get_secrets_manager_client
from security_models import secret_text, parse_json_secret_value


def parse_json_secret(payload, config=None):
    client = get_secrets_manager_client(config)
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = parse_json_secret_value(secret_text(response))
    return {"secret": value}
