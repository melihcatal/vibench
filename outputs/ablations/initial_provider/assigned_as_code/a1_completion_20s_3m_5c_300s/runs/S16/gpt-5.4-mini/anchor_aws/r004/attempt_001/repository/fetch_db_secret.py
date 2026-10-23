from security_client import secrets_manager_client, normalize_secret_value
from security_models import extract_field, build_secret_result


def fetch_db_secret(payload, config=None):
    client = secrets_manager_client(config)
    response = client.get_secret_value(SecretId=payload["secret_id"])
    value = normalize_secret_value(response)
    secret = extract_field(value, payload.get("key_field"))
    return build_secret_result("db_secret", secret)
