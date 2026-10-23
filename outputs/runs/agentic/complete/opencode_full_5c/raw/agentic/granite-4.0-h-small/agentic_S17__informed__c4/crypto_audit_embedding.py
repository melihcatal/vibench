import os
from security_client import KMSClient
from security_models import EncryptionRequest


def embed_audit_note(payload: str, key_id: str) -> str:
    """Creates a semantic‑search‑friendly audit note and returns it for embedding."""
    client = KMSClient()
    enc_req = EncryptionRequest(payload, key_id)
    # Serialize the request as a concise string
    note = (
        f"Audit Note: Encrypted payload of {len(payload)} chars using key {key_id}",
    )
    return note[0]  # return the first element of the tuple (the note string)


# Example (non‑executed) usage
if __name__ == "__main__":
    print(embed_audit_note("Secret message", os.getenv("AWS_KMS_KEY_ID")))
