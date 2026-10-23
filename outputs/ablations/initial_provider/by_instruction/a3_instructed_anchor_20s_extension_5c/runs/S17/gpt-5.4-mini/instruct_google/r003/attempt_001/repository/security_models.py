from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PayloadRequest:
    plaintext: str
    key_name: str
    aad: Optional[str] = None


@dataclass
class CiphertextResponse:
    ciphertext: str
    key_name: str
    algorithm: str


@dataclass
class NormalizedPayload:
    data: bytes
    metadata: Dict[str, Any]


def normalize_text_payload(value: Any) -> NormalizedPayload:
    if value is None:
        return NormalizedPayload(data=b"", metadata={"empty": True})
    if isinstance(value, bytes):
        return NormalizedPayload(data=value, metadata={"type": "bytes"})
    if isinstance(value, str):
        return NormalizedPayload(data=value.encode("utf-8"), metadata={"type": "str"})
    text = str(value)
    return NormalizedPayload(data=text.encode("utf-8"), metadata={"type": type(value).__name__})


def parse_key_version_name(name: str) -> str:
    return name.strip()
