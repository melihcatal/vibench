import dataclasses
from typing import Optional


@dataclasses.dataclass
class EncryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: bytes


@dataclasses.dataclass
class DecryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    ciphertext: bytes


@dataclasses.dataclass
class EnvelopeEncryptionRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: bytes


@dataclasses.dataclass
class SignRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    message: bytes


@dataclasses.dataclass
class VerifyRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    message: bytes
    signature: bytes
