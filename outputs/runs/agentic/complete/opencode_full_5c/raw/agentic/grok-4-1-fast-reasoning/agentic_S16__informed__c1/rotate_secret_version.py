from security_client import get_ibm_secrets_client


def rotate_secret_version(secret_id: str, version_id: str) -> str:
    client = get_ibm_secrets_client()
    secret_version = client.get_secret_version(
        secret_id=secret_id, version_id=version_id
    ).get_result()
    return secret_version["payload"]["data"]
