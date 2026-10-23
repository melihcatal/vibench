from dataclasses import dataclass

@dataclass
class EncryptionRequest:
    plaintext: str
    key_id: str

@dataclass
class EncryptionResponse:
    ciphertext: bytes
    key_id: str

@dataclass
class DecryptionRequest:
    ciphertext: bytes
    key_id: str = None  # Key ID might be embedded in ciphertext or derived

@dataclass
class DecryptionResponse:
    plaintext: str

@dataclass
class SignatureRequest:
    message: str
    key_id: str

@dataclass
class SignatureResponse:
    signature: bytes
    key_id: str

@dataclass
class VerificationRequest:
    message: str
    signature: bytes
    key_id: str

@dataclass
class VerificationResponse:
    is_valid: bool

