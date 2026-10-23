from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
import json


@dataclass
class EncryptionResult:
    ciphertext: bytes
    key_id: str
    algorithm: str
    additional_authenticated_data: Optional[bytes] = None


@dataclass
class DecryptionResult:
    plaintext: bytes
    key_id: str
    algorithm: str


@dataclass
class SigningResult:
    signature: bytes
    key_id: str
    algorithm: str


@dataclass
class VerificationResult:
    success: bool
    key_id: str
    algorithm: str


@dataclass
class EnvelopeEncryptionResult:
    ciphertext: bytes
    encrypted_data_key: bytes
    key_id: str
    algorithm: str
    iv: Optional[bytes] = None


def normalize_payload(payload: Union[str, bytes, Dict[str, Any]]) -> bytes:
    """Normalizes payload to bytes for encryption operations."""
    if isinstance(payload, bytes):
        return payload
    elif isinstance(payload, str):
        return payload.encode("utf-8")
    elif isinstance(payload, dict):
        return json.dumps(payload).encode("utf-8")
    else:
        raise ValueError("Unsupported payload type")


def serialize_envelope_result(result: EnvelopeEncryptionResult) -> Dict[str, Any]:
    """Serializes envelope encryption result for storage or transmission."""
    return {
        "ciphertext": result.ciphertext.hex(),
        "encrypted_data_key": result.encrypted_data_key.hex(),
        "key_id": result.key_id,
        "algorithm": result.algorithm,
        "iv": result.iv.hex() if result.iv else None,
    }


def deserialize_envelope_result(serialized: Dict[str, Any]) -> EnvelopeEncryptionResult:
    """Deserializes envelope encryption result from storage or transmission."""
    return EnvelopeEncryptionResult(
        ciphertext=bytes.fromhex(serialized["ciphertext"]),
        encrypted_data_key=bytes.fromhex(serialized["encrypted_data_key"]),
        key_id=serialized["key_id"],
        algorithm=serialized["algorithm"],
        iv=bytes.fromhex(serialized["iv"]) if serialized.get("iv") else None,
    )
