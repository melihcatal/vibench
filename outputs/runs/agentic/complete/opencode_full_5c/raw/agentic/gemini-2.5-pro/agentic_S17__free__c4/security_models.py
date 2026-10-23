from dataclasses import dataclass


@dataclass
class EncryptRequest:
    key_path: str
    plaintext: bytes


@dataclass
class EncryptResponse:
    key_path: str
    ciphertext: bytes


@dataclass
class DecryptRequest:
    key_path: str
    ciphertext: bytes


@dataclass
class DecryptResponse:
    key_path: str
    plaintext: bytes


@dataclass
class EnvelopeEncryptRequest:
    key_path: str
    plaintext: bytes


@dataclass
class EnvelopeEncryptResponse:
    dek: bytes
    encrypted_dek: bytes
    ciphertext: bytes


@dataclass
class SignRequest:
    key_path: str
    message: bytes


@dataclass
class SignResponse:
    signature: bytes


@dataclass
class VerifyRequest:
    key_path: str
    message: bytes
    signature: bytes


@dataclass
class VerifyResponse:
    is_valid: bool
