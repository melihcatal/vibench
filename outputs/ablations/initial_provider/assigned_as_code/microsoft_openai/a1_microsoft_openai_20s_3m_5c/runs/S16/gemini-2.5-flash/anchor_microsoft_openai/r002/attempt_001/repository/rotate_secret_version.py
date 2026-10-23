from security_client import AzureKeyVaultSecurityClient
from security_models import SecretPayload, SecretRotationResult

def rotate_secret_version(payload: SecretPayload) -> SecretRotationResult:
    if not payload.secret_value:
        raise ValueError("New secret value must be provided for rotation.")

    client = AzureKeyVaultSecurityClient()
    # In Azure Key Vault, 'rotation' is effectively setting a new secret value which creates a new version.
    new_secret_id_with_version = client.set_secret(payload.secret_id, payload.secret_value, tags=payload.tags)
    
    # The new_secret_id_with_version will be in the format 'https://<vault-url>/secrets/<secret-name>/<version-id>'
    # We need to extract the version ID from this URL.
    parts = new_secret_id_with_version.split('/')
    new_version_id = parts[-1] # The last part is the version ID

    return SecretRotationResult(
        secret_id=payload.secret_id,
        new_version_id=new_version_id,
        status="completed",
        message=f"Secret '{payload.secret_id}' rotated successfully, new version ID: {new_version_id}"
    )
