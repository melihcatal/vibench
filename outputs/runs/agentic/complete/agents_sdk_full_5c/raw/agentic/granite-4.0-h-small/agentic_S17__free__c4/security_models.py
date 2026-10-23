from typing import TypedDict, Any, Dict

class EnvelopeEncryptionRequest(TypedDict):
    payload: str
    bucket: str
    blob: str
    project_id: str
    location: str
    key_ring: str
    crypto_key: str

class EnvelopeEncryptionResponse(TypedDict):
    ciphertext_blob: str
    wrapped_key: str

class KeyUsageEvent(TypedDict):
    key_name: str
    operation: str   # e.g., 'ENCRYPT', 'DECRYPT', 'SIGN', 'VERIFY'\n    timestamp: str   # ISO 8601 UTC timestamp\n    context: Dict[str, Any]  # free-form metadata (e.g., bucket, blob, user_id)\n
class ComplianceNote(TypedDict):
    note_id: str
    title: str
    description: str
    severity: str  # e.g., 'HIGH', 'MEDIUM', 'LOW'\n    recommendation: str
