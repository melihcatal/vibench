from security_client import AzureKeyVaultSecurityClient
from security_models import SecretSummary
from typing import List

def rotation_summary() -> List[SecretSummary]:
    client = AzureKeyVaultSecurityClient()
    secrets_summary = []

    for secret_properties in client.list_properties_of_secrets():
        # Fetching the full secret to get more properties, or directly using secret_properties
        # Azure Key Vault's list_properties_of_secrets provides most of what we need for a summary.
        # We can also get the latest version if needed.

        # For simplicity, we are using the properties directly from list_properties_of_secrets
        # For a true 'latest version id', we might need to get the secret itself.
        
        # The `expires_on` and `created_on` are datetime objects, converting to string for serialization
        expires_on_str = secret_properties.expires_on.isoformat() if secret_properties.expires_on else None
        created_on_str = secret_properties.created_on.isoformat() if secret_properties.created_on else None

        summary = SecretSummary(
            secret_id=secret_properties.name,
            created_on=created_on_str,
            expires_on=expires_on_str,
            enabled=secret_properties.enabled if secret_properties.enabled is not None else False,
            tags=secret_properties.tags,
            latest_version_id=secret_properties.version,
            latest_version_enabled=secret_properties.enabled
        )
        secrets_summary.append(summary)
    return secrets_summary
