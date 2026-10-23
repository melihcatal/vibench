from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass
from enum import Enum
import json


class EncryptionAlgorithm(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSAES_OAEP_SHA_1 = "RSAES_OAEP_SHA_1"
    RSAES_OAEP_SHA_256 = "RSAES_OAEP_SHA_256"


class SigningAlgorithm(str, Enum):
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    RSASSA_PSS_SHA_384 = "RSASSA_PSS_SHA_384"
    RSASSA_PSS_SHA_512 = "RSASSA_PSS_SHA_512"
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    RSASSA_PKCS1_V1_5_SHA_384 = "RSASSA_PKCS1_V1_5_SHA_384"
    RSASSA_PKCS1_V1_5_SHA_512 = "RSASSA_PKCS1_V1_5_SHA_512"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    ECDSA_SHA_384 = "ECDSA_SHA_384"
    ECDSA_SHA_512 = "ECDSA_SHA_512"


@dataclass
class EncryptionRequest:
    plaintext: Union[str, bytes, Dict[str, Any]]
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plaintext": self.plaintext
            if isinstance(self.plaintext, (str, bytes))
            else json.dumps(self.plaintext),
            "key_id": self.key_id,
            "encryption_context": self.encryption_context,
            "algorithm": self.algorithm.value,
        }


@dataclass
class EncryptionResponse:
    ciphertext_blob: bytes
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext_blob": self.ciphertext_blob.hex(),
            "key_id": self.key_id,
            "encryption_context": self.encryption_context,
        }


@dataclass
class DecryptionRequest:
    ciphertext_blob: bytes
    encryption_context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext_blob": self.ciphertext_blob.hex(),
            "encryption_context": self.encryption_context,
        }


@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plaintext": self.plaintext.hex(),
            "key_id": self.key_id,
            "encryption_algorithm": self.encryption_algorithm,
        }


@dataclass
class SignRequest:
    message: Union[str, bytes]
    key_id: str
    algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256
    message_type: str = "RAW"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message
            if isinstance(self.message, bytes)
            else self.message.encode("utf-8"),
            "key_id": self.key_id,
            "algorithm": self.algorithm.value,
            "message_type": self.message_type,
        }


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    algorithm: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature": self.signature.hex(),
            "key_id": self.key_id,
            "algorithm": self.algorithm,
        }


@dataclass
class VerifyRequest:
    message: Union[str, bytes]
    signature: bytes
    key_id: str
    algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256
    message_type: str = "RAW"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message
            if isinstance(self.message, bytes)
            else self.message.encode("utf-8"),
            "signature": self.signature,
            "key_id": self.key_id,
            "algorithm": self.algorithm.value,
            "message_type": self.message_type,
        }


@dataclass
class VerifyResponse:
    is_valid: bool
    key_id: str
    algorithm: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "key_id": self.key_id,
            "algorithm": self.algorithm,
        }


@dataclass
class EnvelopeEncryptionRequest:
    data_key_spec: str = "AES_256"
    encryption_context: Optional[Dict[str, str]] = None
    key_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data_key_spec": self.data_key_spec,
            "encryption_context": self.encryption_context,
            "key_id": self.key_id,
        }


@dataclass
class EnvelopeEncryptionResponse:
    ciphertext_blob: bytes
    plaintext_key: bytes
    key_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext_blob": self.ciphertext_blob.hex(),
            "plaintext_key": self.plaintext_key.hex(),
            "key_id": self.key_id,
        }
