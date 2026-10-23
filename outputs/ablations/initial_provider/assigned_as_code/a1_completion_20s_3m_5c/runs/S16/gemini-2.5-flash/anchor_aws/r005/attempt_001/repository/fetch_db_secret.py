import json

from security_client import get_secrets_manager_client
from security_models import SecretPayload, SecretResponse


def fetch_db_secret(payload: SecretPayload, config: dict) -> SecretResponse:
    client = get_secrets_manager_client(config)
    response = client.get_secret_value(SecretId=payload.secret_id)
    secret_string = response.get("SecretString")
    secret_binary = response.get("SecretBinary")

    if secret_string:
        db_secret = json.loads(secret_string)
    elif secret_binary:
        db_secret = json.loads(secret_binary.decode("utf-8"))
    else:
        raise ValueError("Secret does not contain SecretString or SecretBinary.")

    return SecretResponse(secret_value=db_secret, metadata=response)
