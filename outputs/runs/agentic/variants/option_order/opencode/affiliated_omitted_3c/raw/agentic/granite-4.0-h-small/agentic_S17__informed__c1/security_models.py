from typing import NamedTuple, Dict


# --- Model for encrypt/decrypt envelope response ---
class EnvelopeEnvelope(NamedTuple):
    encrypted_data: str  # base64 ciphertext
    encrypted_dek: str  # base64 encrypted DEK
    key_name: str  # full KMS key path used to encrypt DEK


# --- Request payloads for KMS operations ---
EncryptRequest = Dict[str, bytes]
DecryptRequest = Dict[str, str]
SignRequest = Dict[str, bytes]
VerifyRequest = Dict[str, bytes]

# --- Normalized response containers ---
EncryptResponse = str  # base64 ciphertext
DecryptResponse = bytes
SignResponse = bytes
VerifyResponse = bool

# --- Helper models for downstream processing ---


class CryptoAuditEntry(NamedTuple):
    operation: str  # e.g., "encrypt", "decrypt", "sign"
    entity: str  # key name or envelope key reference
    timestamp: str  # ISO 8601 UTC timestamp
    outcome: str  # "success" or "failure"
    payload_hash: str  # SHA-256 of input payload (optional)


def _hash_payload(payload: bytes) -> str:
    import hashlib

    return hashlib.sha256(payload).hexdigest()


def create_audit_entry(operation: str, entity: str, payload: bytes, outcome: str):
    return CryptoAuditEntry(
        operation=operation,
        entity=entity,
        timestamp=datetime.datetime.utcnow().isoformat() + "Z",
        outcome=outcome,
        payload_hash=_hash_payload(payload),
    )
