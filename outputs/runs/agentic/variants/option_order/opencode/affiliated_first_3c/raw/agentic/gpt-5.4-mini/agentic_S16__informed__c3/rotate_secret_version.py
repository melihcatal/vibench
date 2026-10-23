from security_client import create_secrets_manager_client, get_secret_name
from security_models import normalize_secret_value


def rotate_secret_version(
    version_id: str | None = None, stage: str | None = None
) -> str:
    client = create_secrets_manager_client()
    secret_id = get_secret_name("rotating-secret")
    kwargs = {"SecretId": secret_id}
    if version_id:
        kwargs["VersionId"] = version_id
    if stage:
        kwargs["VersionStage"] = stage
    response = client.get_secret_value(**kwargs)
    return normalize_secret_value(
        response.get("SecretString") or response.get("SecretBinary")
    )
