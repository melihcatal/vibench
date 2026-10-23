from security_client import get_secret_client
from ibm_secrets_manager_sdk.models import SecretMetadata

def persist_audit_note(secret_id: str, audit_text: str) -> None:
    """Persist a human‑readable audit note alongside a secret.

    The note is stored as a label called 'audit_note' so that downstream
    semantic search can retrieve it.
    """
    client = get_secret_client()
    # Update secret metadata to add/overwrite the audit_note label
    client.update_secret_metadata(
        secret_id=secret_id,
        metadata_patch={'labels': {'audit_note': audit_text}}
    ).get_result()

# Example usage
if __name__ == "__main__":
    persist_audit_note('my-secret', 'Rotation performed on 2025-08-20; replaced with new API key.')