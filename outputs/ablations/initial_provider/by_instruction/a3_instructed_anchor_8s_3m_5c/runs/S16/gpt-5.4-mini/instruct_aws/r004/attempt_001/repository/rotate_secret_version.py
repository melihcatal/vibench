from security_client import load_secret_name, secrets_manager_client
from security_models import normalize_secret_payload


def read_secret_version(secret_name: str = None, version_stage: str = None, version_id: str = None):
    client = secrets_manager_client()
    secret_id = secret_name or load_secret_name("rotation/secret")
    kwargs = {"SecretId": secret_id}
    if version_stage:
        kwargs["VersionStage"] = version_stage
    if version_id:
        kwargs["VersionId"] = version_id
    response = client.get_secret_value(**kwargs)
    return normalize_secret_payload(response)["value"]
