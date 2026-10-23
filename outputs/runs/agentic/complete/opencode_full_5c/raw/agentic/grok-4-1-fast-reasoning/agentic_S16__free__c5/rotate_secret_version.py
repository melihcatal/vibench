from security_client import SecurityClient
from security_models import SecretResponse


def rotate_secret_version(
    secret_name: str = "prod/rotatable-secret", version_stage: str = "AWSPREVIOUS"
) -> SecretResponse:
    client = SecurityClient()
    return client.get_secret(secret_name, version_stage)
