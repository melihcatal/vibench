from dataclasses import dataclass
from typing import Any, Optional


def normalize_bytes(value):
    if value is None:
        return b''
    if isinstance(value, bytes):
        return value
    return str(value).encode('utf-8')


def normalize_plaintext(value):
    return normalize_bytes(value)


@dataclass
class EncryptRequest:
    plaintext: Any
    key_id: Optional[str] = None
    encryption_context: Optional[dict] = None


@dataclass
class EncryptResponse:
    ciphertext: Any
    key_id: str
    encryption_algorithm: str
    def to_dict(self): return {'ciphertext': self.ciphertext, 'key_id': self.key_id, 'encryption_algorithm': self.encryption_algorithm}


@dataclass
class DecryptRequest:
    ciphertext_blob: Any
    encryption_context: Optional[dict] = None


@dataclass
class DecryptResponse:
    plaintext: Any
    key_id: str
    encryption_algorithm: str
    def to_dict(self): return {'plaintext': self.plaintext, 'key_id': self.key_id, 'encryption_algorithm': self.encryption_algorithm}


@dataclass
class EnvelopeEncryptRequest:
    plaintext: Any
    key_id: Optional[str] = None
    encryption_context: Optional[dict] = None


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: Any
    nonce: Any
    ciphertext: Any
    key_id: str
    def to_dict(self): return {'encrypted_data_key': self.encrypted_data_key, 'nonce': self.nonce, 'ciphertext': self.ciphertext, 'key_id': self.key_id}


@dataclass
class SignRequest:
    message: str
    key_id: Optional[str] = None


@dataclass
class VerifyRequest:
    message: str
    key_id: Optional[str] = None
    signature: Any = None


@dataclass
class SignResponse:
    signature: Any
    key_id: str
    signing_algorithm: str
    def to_dict(self): return {'signature': self.signature, 'key_id': self.key_id, 'signing_algorithm': self.signing_algorithm}


@dataclass
class VerifyResponse:
    verified: bool
    key_id: str
    signing_algorithm: str
    def to_dict(self): return {'verified': self.verified, 'key_id': self.key_id, 'signing_algorithm': self.signing_algorithm}
