from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_ciphertext(value: str) -> str:
    return value.strip()


@dataclass
class EncryptRequest:
    plaintext: str
    key_id: str


@dataclass
class EncryptResponse:
    provider: str
    key_id: str
    ciphertext: str
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DecryptRequest:
    ciphertext: str
    key_id: str


@dataclass
class DecryptResponse:
    provider: str
    key_id: str
    plaintext: str
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_id: str
    context: Dict[str, str]


@dataclass
class EnvelopeEncryptResponse:
    provider: str
    key_id: str
    ciphertext: str
    encrypted_data_key: str
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
