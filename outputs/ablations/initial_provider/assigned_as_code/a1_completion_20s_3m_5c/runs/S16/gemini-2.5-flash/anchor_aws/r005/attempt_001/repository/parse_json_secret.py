import json

from security_client import get_secrets_manager_client
from security_models import SecretPayload, SecretResponse


def parse_json_secret(payload: SecretPayload, config: dict) -> SecretResponse:
    client = get_secrets_manager_client(config)
    
    # Construct the arguments for get_secret_value
    kwargs = {
        "SecretId": payload.secret_id
    }
    if payload.version_id:
        kwargs["VersionId"] = payload.version_id
    if payload.version_stage:
        kwargs["VersionStage"] = payload.version_stage

    response = client.get_secret_value(**kwargs)
    secret_value = response.get("SecretString") or response.get("SecretBinary").decode("utf-8")

    if secret_value:
        parsed_secret = json.loads(secret_value)
        if payload.key_field:
            parsed_secret = parsed_secret[payload.key_field]
        return SecretResponse(secret_value=parsed_secret, metadata=response)
    else:
        raise ValueError("Secret does not contain SecretString or SecretBinary.")
