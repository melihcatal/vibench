import os

from security_client import get_secrets_client, normalize_secret_response


def rotate_secret_version(
    secret_id: str = None, version_stage: str = None, version_id: str = None
):
    client = get_secrets_client()
    secret_id = secret_id or os.getenv("AWS_SECRET_ROTATE_ID", "rotation/secret")
    params = {"SecretId": secret_id}
    if version_stage:
        params["VersionStage"] = version_stage
    if version_id:
        params["VersionId"] = version_id
    response = client.get_secret_value(**params)
    return normalize_secret_response(response)
