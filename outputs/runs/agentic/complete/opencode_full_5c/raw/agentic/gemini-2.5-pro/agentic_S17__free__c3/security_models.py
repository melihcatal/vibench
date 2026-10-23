from dataclasses import dataclass
from typing import Optional


@dataclass
class EncryptionPayload:
    data: bytes
    key_id: str


@dataclass
class DecryptionPayload:
    ciphertext: bytes
    key_id: str


@dataclass
class AuditEvent:
    event_name: str
    event_time: str
    username: str
    resource_name: str
