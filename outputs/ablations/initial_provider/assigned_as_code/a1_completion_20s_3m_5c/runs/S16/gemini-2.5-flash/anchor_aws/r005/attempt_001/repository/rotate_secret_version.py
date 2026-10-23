from security_client import get_secrets_manager_client
from security_models import SecretPayload, SecretResponse


def rotate_secret_version(payload: SecretPayload, config: dict) -> SecretResponse:
    if not payload.version_id and not payload.version_stage:
        raise ValueError("Either version_id or version_stage must be provided to read a specific secret version.")

    client = get_secrets_manager_client(config)
    
    kwargs = {
        "SecretId": payload.secret_id
    }
    if payload.version_id:
        kwargs["VersionId"] = payload.version_id
    if payload.version_stage:
        kwargs["VersionStage"] = payload.version_stage

    response = client.get_secret_value(**kwargs)
    secret_value = response.get("SecretString") or response.get("SecretBinary").decode("utf-8")

    return SecretResponse(secret_value=secret_value, metadata=response)
