from secret_clients import SecretsManagerClient


def rotate_secret_version(secret_id: str, version_stage: str = "AWSCURRENT") -> dict:
    """Reads a specific secret version or staged value from IBM Cloud Secrets Manager.
    Args:
        secret_id (str): ID of the secret.
        version_stage (str): Stage label of the version to retrieve (default: 'AWSCURRENT').
    Returns:
        dict: The retrieved secret version data.
    """
    client = SecretsManagerClient()
    return client.get_secret_value(SecretId=secret_id, VersionStage=version_stage)
