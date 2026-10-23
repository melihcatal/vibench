from dataclasses import dataclass
from typing import Any, Dict, Optional


# Representation of a request payload for encryption/decryption operations
@dataclass
class CryptoRequest:
    plaintext: Optional[str] = None
    ciphertext: Optional[str] = None
    key_id: Optional[str] = None
    encrypted_data_key: Optional[str] = None
    signature: Optional[str] = None
    verification_result: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Normalized response shapes used by various helper utilities
@dataclass
class EncryptionResult:
    ciphertext_blob: str  # base64 encoded blob
    encrypted_data_key: Optional[str] = None  # base64 encoded if envelope encrypt
    key_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "CiphertextBlob": self.ciphertext_blob,
            "EncryptedDataKey": self.encrypted_data_key,
            "KeyId": self.key_id,
        }


@dataclass
class DecryptionResult:
    plaintext: str
    key_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"Plaintext": self.plaintext, "KeyId": self.key_id}


@dataclass
class SignatureResult:
    signature: str  # base64 encoded
    key_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"Signature": self.signature, "KeyId": self.key_id}


@dataclass
class VerificationResult:
    verified: bool
    key_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"Verified": self.verified, "KeyId": self.key_id}


# Simple logger wrapper that can be swapped for more sophisticated systems
class Logger:
    @staticmethod
    def info(msg: str):
        print(f"[INFO] {msg}")

    @staticmethod
    def warn(msg: str):
        print(f"[WARN] {msg}")

    @staticmethod
    def error(msg: str):
        print(f"[ERROR] {msg}")
