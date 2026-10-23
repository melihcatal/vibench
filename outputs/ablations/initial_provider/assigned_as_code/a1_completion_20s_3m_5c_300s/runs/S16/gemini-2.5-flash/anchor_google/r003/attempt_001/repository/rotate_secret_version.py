from google.cloud import secretmanager
from security_client import SecretManagerClient
from security_models import RotateSecretPayload, SecretVersionOutput

def rotate_secret_version(payload: RotateSecretPayload) -> SecretVersionOutput:
    client = SecretManagerClient()

    # In Google Secret Manager, 'rotation' typically means adding a new secret version.
    # The new_secret_data will become the payload of the new version.
    new_version_name = client.add_secret_version(
        project_id=payload.project_id,
        secret_id=payload.secret_id,
        payload_data=payload.new_secret_data
    )

    # Extract version ID from the full resource name
    version_id = new_version_name.split('/')[-1]

    # Get information about the newly created version
    version_response = client._client.get_secret_version(request={
        "name": new_version_name
    })

    return SecretVersionOutput(
        secret_id=payload.secret_id,
        version=version_id,
        state=str(version_response.state).split('.')[-1], # e.g., STATE_ENABLED -> ENABLED
        create_time=version_response.create_time.isoformat(),
        destroy_time=version_response.destroy_time.isoformat() if version_response.destroy_time else None
    )
