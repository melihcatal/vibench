import json
from dataclasses import dataclass, asdict
from typing import Any

@dataclass

class PlaintextEnvelope:
    """Representation of envelope‑encrypted payload for serialization."""
    ciphertext: bytes
    data_key: dict[str, Any]  # contains ciphertext_blob and optional plaintext_key

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'PlaintextEnvelope':
        return cls(**data)

@dataclass

class CiphertextEnvelope:
    """Intermediate model for received envelope data (already parsed JSON)."""
    ciphertext: bytes
    data_key: dict[str, str]  # e.g., ciphertext_blob (hex or base64) and plaintext_key (hex)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'CiphertextEnvelope':
        # Convert bytes from base64 or hex if needed – kept simple for demo
        return cls(ciphertext=bytes.fromhex(data['ciphertext']),
                   data_key=dict(ciphertext_blob=data['data_key']['ciphertext_blob'],
                                 plaintext_key=data['data_key']['plaintext_key']))
