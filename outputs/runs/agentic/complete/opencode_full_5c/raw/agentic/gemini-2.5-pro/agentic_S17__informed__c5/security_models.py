from dataclasses import dataclass
import base64


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: bytes


@dataclass
class EncryptionResponse:
    key_id: str
    ciphertext: bytes

    def to_base64(self) -> str:
        return base64.b64encode(self.ciphertext).decode("utf-8")


@dataclass
class DecryptionRequest:
    key_id: str
    ciphertext: bytes


@dataclass
class DecryptionResponse:
    key_id: str
    plaintext: bytes

    def to_string(self) -> str:
        return self.plaintext.decode("utf-8")


@dataclass
class SigningRequest:
    key_id: str
    message: bytes
    signing_algorithm: str


@dataclass
class SigningResponse:
    key_id: str
    signature: bytes
    signing_algorithm: str


@dataclass
class VerificationRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str


@dataclass
class VerificationResponse:
    key_id: str
    is_valid: bool
