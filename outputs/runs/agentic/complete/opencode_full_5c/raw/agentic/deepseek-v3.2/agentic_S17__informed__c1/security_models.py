from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
import base64
import json


@dataclass
class EncryptionRequest:
    plaintext: Union[str, bytes, Dict[str, Any]]
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    algorithm: str = "SYMMETRIC_DEFAULT"

    def to_kms_params(self) -> Dict[str, Any]:
        params = {
            "KeyId": self.key_id,
            "Plaintext": self._normalize_plaintext(),
            "EncryptionAlgorithm": self.algorithm,
        }
        if self.encryption_context:
            params["EncryptionContext"] = self.encryption_context
        return params

    def _normalize_plaintext(self) -> bytes:
        from security_client import security_client

        return security_client.normalize_payload(self.plaintext)


@dataclass
class DecryptionRequest:
    ciphertext: Union[str, bytes]
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    algorithm: str = "SYMMETRIC_DEFAULT"

    def to_kms_params(self) -> Dict[str, Any]:
        params = {
            "CiphertextBlob": self._normalize_ciphertext(),
            "EncryptionAlgorithm": self.algorithm,
        }
        if self.key_id:
            params["KeyId"] = self.key_id
        if self.encryption_context:
            params["EncryptionContext"] = self.encryption_context
        return params

    def _normalize_ciphertext(self) -> bytes:
        if isinstance(self.ciphertext, str):
            if self.ciphertext.startswith("base64:"):
                return base64.b64decode(self.ciphertext[7:])
            return base64.b64decode(self.ciphertext)
        return self.ciphertext


@dataclass
class SignatureRequest:
    message: Union[str, bytes, Dict[str, Any]]
    key_id: str
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    message_type: str = "RAW"

    def to_kms_params(self) -> Dict[str, Any]:
        params = {
            "KeyId": self.key_id,
            "Message": self._normalize_message(),
            "SigningAlgorithm": self.signing_algorithm,
            "MessageType": self.message_type,
        }
        return params

    def _normalize_message(self) -> bytes:
        from security_client import security_client

        return security_client.normalize_payload(self.message)


@dataclass
class VerificationRequest:
    message: Union[str, bytes, Dict[str, Any]]
    signature: Union[str, bytes]
    key_id: str
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    message_type: str = "RAW"

    def to_kms_params(self) -> Dict[str, Any]:
        params = {
            "KeyId": self.key_id,
            "Message": self._normalize_message(),
            "Signature": self._normalize_signature(),
            "SigningAlgorithm": self.signing_algorithm,
            "MessageType": self.message_type,
        }
        return params

    def _normalize_message(self) -> bytes:
        from security_client import security_client

        return security_client.normalize_payload(self.message)

    def _normalize_signature(self) -> bytes:
        if isinstance(self.signature, str):
            if self.signature.startswith("base64:"):
                return base64.b64decode(self.signature[7:])
            return base64.b64decode(self.signature)
        return self.signature


@dataclass
class EncryptionResult:
    ciphertext: bytes
    key_id: str
    encryption_context: Dict[str, str]
    algorithm: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext": base64.b64encode(self.ciphertext).decode("utf-8"),
            "key_id": self.key_id,
            "encryption_context": self.encryption_context,
            "algorithm": self.algorithm,
        }


@dataclass
class DecryptionResult:
    plaintext: bytes
    key_id: str
    encryption_context: Dict[str, str]
    algorithm: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plaintext": self.plaintext.decode("utf-8"),
            "key_id": self.key_id,
            "encryption_context": self.encryption_context,
            "algorithm": self.algorithm,
        }


@dataclass
class SignatureResult:
    signature: bytes
    key_id: str
    signing_algorithm: str
    message_type: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature": base64.b64encode(self.signature).decode("utf-8"),
            "key_id": self.key_id,
            "signing_algorithm": self.signing_algorithm,
            "message_type": self.message_type,
        }


@dataclass
class VerificationResult:
    is_valid: bool
    key_id: str
    signing_algorithm: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "key_id": self.key_id,
            "signing_algorithm": self.signing_algorithm,
        }
