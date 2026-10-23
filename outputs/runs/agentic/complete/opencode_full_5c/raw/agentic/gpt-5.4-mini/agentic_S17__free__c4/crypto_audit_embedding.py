from security_client import SecurityClient


def crypto_audit_embedding(note: str) -> dict:
    client = SecurityClient()
    vector = [float((ord(ch) % 13) / 13.0) for ch in note[:16]]
    return {
        "provider": client.provider,
        "key_id": client.managed_key_id(),
        "embedding": vector,
    }
