from security_client import get_secrets_manager_client
from security_models import secret_text, parse_json_secret_value


def fetch_db_secret(payload, config=None):
    client = get_secrets_manager_client(config)
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = secret_text(response)
    secret = parse_json_secret_value(value)
    if isinstance(secret, dict):
        return {"db_secret": secret.get(payload.get("key_field", "connection_string"), secret)}
    return {"db_secret": secret}
