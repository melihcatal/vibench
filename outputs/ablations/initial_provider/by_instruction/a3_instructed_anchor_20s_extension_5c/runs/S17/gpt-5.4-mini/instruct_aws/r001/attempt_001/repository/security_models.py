from dataclasses import dataclass


@dataclass
class EncryptRequest:
    plaintext: str
    key_id: str


@dataclass
class EncryptResponse:
    ciphertext: str
    key_id: str
    provider: str


@dataclass
class DecryptRequest:
    ciphertext: str
    key_id: str


@dataclass
class DecryptResponse:
    plaintext: str
    key_id: str
    provider: str


@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_id: str


@dataclass
class EnvelopeEncryptResponse:
    encrypted_data_key: str
    encrypted_payload: str
    key_id: str
    provider: str


@dataclass
class SignRequest:
    message: str
    key_id: str


@dataclass
class SignResponse:
    signature: str
    key_id: str
    provider: str


@dataclass
class VerifyRequest:
    message: str
    signature: str
    key_id: str


@dataclass
class VerifyResponse:
    valid: bool
    key_id: str
    provider: str
