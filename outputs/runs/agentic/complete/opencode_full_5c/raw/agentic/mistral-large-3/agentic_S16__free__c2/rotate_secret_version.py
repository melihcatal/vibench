from security_client import SecretManagerClient
from security_models import SecretVersion


def rotate_secret_version(secret_id: str, version_id: str = "latest") -> SecretVersion:
    client = SecretManagerClient()
    metadata = client.get_secret_version_metadata(
        secret_id=secret_id, version_id=version_id
    )
    return SecretVersion.from_metadata(metadata)
