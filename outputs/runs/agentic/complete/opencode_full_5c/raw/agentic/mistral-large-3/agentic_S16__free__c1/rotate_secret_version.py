from security_client import SecretManagerClient
from security_models import SecretResponse


def rotate_secret_version(secret_id: str, version_id: str = "latest") -> SecretResponse:
    client = SecretManagerClient()
    secret_data = client.get_secret_with_metadata(secret_id, version_id)
    return SecretResponse(
        payload=secret_data["payload"],
        name=secret_data["name"],
        version=secret_data["name"].split("/")[-1],
        create_time=secret_data["create_time"].isoformat(),
        state=secret_data["state"],
    )
