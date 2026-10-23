import os
from ibm_secrets_manager_sdk import SecretsManagerV1


def rotate_secret_version(secret_name: str, version_to_stage: str) -> str:
    """Rotate a secret by staging a new version and promoting it.
    Args:
        secret_name: Name/ID of the secret.
        version_to_stage: The version payload (as string) to stage as the next version.
    Returns:
        Identifier of the newly promoted version.
    """
    api_key = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
    service_url = os.getenv("IBM_SECRETS_MANAGER_URL")
    client = SecretsManagerV1.new_instance(api_key=api_key, service_url=service_url)
    # 1. Stage the new version
    stage_resp = client.stage_secret_version(
        secret_type="arbitrary",
        id=secret_name,
        secret_value=version_to_stage,
    ).get_result()
    staged_ver = stage_resp.get("staged_version_id")
    # 2. Promote the staged version to active
    promote_resp = client.promote_secret_version(
        secret_type="arbitrary",
        id=secret_name,
        staged_version_id=staged_ver,
    ).get_result()
    promoted_ver = promote_resp.get("active_version_id")
    return promoted_ver
