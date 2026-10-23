from security_models import SecretAuditNote
from security_client import SecretsManagerClient
import json


def embed_audit_note(secret_name: str, note_text: str) -> None:
    """Embeds secret audit notes for semantic search.

    Stores the note alongside the secret metadata for later retrieval
    and semantic search against the audit history.

    Args:
        secret_name: Name of the secret to annotate.
        note_text: Human-readable audit entry.
    """
    client = SecretsManagerClient()
    # Retrieve current metadata, append new note, update secret
    metadata = client.get_secret_metadata(name=secret_name)
    audit_notes = metadata.get("audit_notes", [])
    audit_notes.append(
        SecretAuditNote(timestamp=str(int(time.time())), note=note_text).to_dict()
    )
    client.update_secret_metadata(
        name=secret_name, metadata={"audit_notes": audit_notes}
    )


if __name__ == "__main__":
    embed_audit_note(
        os.getenv("AUDIT_SECRET_NAME"),
        "Rotated API key as part of quarterly compliance run",
    )
    print("Audit note embedded")
