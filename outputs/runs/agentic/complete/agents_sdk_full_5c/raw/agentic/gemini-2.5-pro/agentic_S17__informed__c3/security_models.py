from dataclasses import dataclass

@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str

@dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: bytes

@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str

@dataclass
class SigningRequest:
    key_id: str
    message: bytes
    signing_algorithm: str

@dataclass
class SigningResponse:
    signature: bytes
    key_id: str

@dataclass
class EnvelopeEncryptionResult:
    encrypted_data: bytes
    encrypted_data_key: bytes
