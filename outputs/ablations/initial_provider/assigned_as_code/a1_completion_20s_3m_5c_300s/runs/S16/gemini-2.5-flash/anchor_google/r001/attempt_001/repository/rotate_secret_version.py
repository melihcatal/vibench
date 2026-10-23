from google.cloud import secretmanager
from security_client import SecretManagerClient
from security_models import SecretPayload, SecretResponse

def rotate_secret_version(payload: SecretPayload, config: dict) -> SecretResponse:
    client = SecretManagerClient()
    project_id = payload.project_id or config.get("project_id")
    if not project_id:
        raise ValueError("Project ID must be provided in payload or config.")

    # In Google Cloud Secret Manager, "rotation" usually involves creating a new version.
    # This function focuses on *accessing* a specific version or staged value (like 'latest').
    secret_version_name = client.get_secret_version_name(
        project_id=project_id,
        secret_id=payload.secret_id,
        version_id=payload.version_id # Can be 'latest', a version number, or a stage like 'AWESOME_SECRET_STAGE'
    )

    response = client.access_secret_version(secret_version_name)
    secret_data = response.payload.data.decode("utf-8")

    return SecretResponse(
        secret_id=payload.secret_id,
        version_id=response.name.split('/')[-1], # The actual version accessed
        data=secret_data
    )
