from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class EncryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: str


@dataclass
class DecryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    ciphertext: str


@dataclass
class EnvelopeEncryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: str


@dataclass
class SignRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    digest: bytes


@dataclass
class VerifyRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    digest: bytes
    signature: bytes


@dataclass
class EncryptionResponse:
    ciphertext: str


@dataclass
class DecryptionResponse:
    plaintext: str


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    ciphertext: str


@dataclass
class SignResponse:
    signature: bytes


@dataclass
class VerifyResponse:
    is_valid: bool
