from security_client import AzureKeyVaultSecurityClient
from security_models import SecretRotationSummary
from datetime import datetime, timedelta
import os

def summarize_secret_rotation(secret_name: str, vault_url: str = None) -> SecretRotationSummary:
    client = AzureKeyVaultSecurityClient(vault_url)
    # Azure Key Vault does not have direct rotation metadata, so we infer from creation/expiration
    # In a real scenario, rotation metadata might be stored as secret tags or in an external system.
    secret_properties = client.client.get_secret_properties(secret_name)

    current_version = secret_properties.id.split('/')[-1]
    last_rotated = secret_properties.created_on.isoformat() if secret_properties.created_on else None

    rotation_status = "unknown"
    next_rotation_due = None

    # Example: Assume secrets should rotate annually if expiration is set
    if secret_properties.expires_on:
        if datetime.now(secret_properties.expires_on.tzinfo) > secret_properties.expires_on:
            rotation_status = "expired"
        else:
            rotation_status = "active"
            next_rotation_due = secret_properties.expires_on.isoformat()
    elif secret_properties.created_on: # If no explicit expiration, assume a 365 day rotation policy for status example
        assumed_expiration = secret_properties.created_on + timedelta(days=365)
        if datetime.now(secret_properties.created_on.tzinfo) > assumed_expiration:
            rotation_status = "overdue"
        else:
            rotation_status = "active"
            next_rotation_due = assumed_expiration.isoformat()

    return SecretRotationSummary(
        secret_id=secret_name,
        current_version=current_version,
        last_rotated=last_rotated,
        next_rotation_due=next_rotation_due,
        rotation_status=rotation_status
    )
