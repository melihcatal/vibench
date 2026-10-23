import os
import base64
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from enum import Enum


class EncryptionAlgorithm(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSAES_OAEP_SHA_1 = "RSAES_OAEP_SHA_1"
    RSAES_OAEP_SHA_256 = "RSAES_OAEP_SHA_256"


class SigningAlgorithm(str, Enum):
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    RSASSA_PSS_SHA_384 = "RSASSA_PSS_SHA_384"
    RSASSA_PSS_SHA_512 = "RSASSA_PSS_SHA_512"
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    ECDSA_SHA_384 = "ECDSA_SHA_384"
    ECDSA_SHA_512 = "ECDSA_SHA_512"


class MessageType(str, Enum):
    RAW = "RAW"
    DIGEST = "DIGEST"


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: str = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    grant_tokens: Optional[List[str]] = None

    def to_aws_params(self) -> Dict[str, Any]:
        params = {
            "KeyId": self.key_id,
            "Plaintext": self.plaintext.encode("utf-8"),
            "EncryptionAlgorithm": self.encryption_algorithm,
        }
        if self.encryption_context:
            params["EncryptionContext"] = self.encryption_context
        if self.grant_tokens:
            params["GrantTokens"] = self.grant_tokens
        return params


@dataclass
class EncryptResponse:
    ciphertext_blob: str
    key_id: str
    encryption_algorithm: str
    ciphertext_blob_bytes: Optional[bytes] = field(default=None, repr=False)

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "EncryptResponse":
        ciphertext_bytes = response["CiphertextBlob"]
        return cls(
            ciphertext_blob=base64.b64encode(ciphertext_bytes).decode("utf-8"),
            key_id=response["KeyId"],
            encryption_algorithm=response.get("EncryptionAlgorithm", ""),
            ciphertext_blob_bytes=ciphertext_bytes,
        )


@dataclass
class DecryptRequest:
    ciphertext_blob: str
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: str = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    grant_tokens: Optional[List[str]] = None

    def to_aws_params(self) -> Dict[str, Any]:
        params = {
            "CiphertextBlob": base64.b64decode(self.ciphertext_blob),
            "EncryptionAlgorithm": self.encryption_algorithm,
        }
        if self.encryption_context:
            params["EncryptionContext"] = self.encryption_context
        if self.grant_tokens:
            params["GrantTokens"] = self.grant_tokens
        return params


@dataclass
class DecryptResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str
    plaintext_bytes: Optional[bytes] = field(default=None, repr=False)

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "DecryptResponse":
        plaintext_bytes = response["Plaintext"]
        return cls(
            plaintext=plaintext_bytes.decode("utf-8"),
            key_id=response["KeyId"],
            encryption_algorithm=response.get("EncryptionAlgorithm", ""),
            plaintext_bytes=plaintext_bytes,
        )


@dataclass
class GenerateDataKeyRequest:
    key_id: str
    key_spec: str = "AES_256"
    encryption_context: Optional[Dict[str, str]] = None
    number_of_bytes: Optional[int] = None

    def to_aws_params(self) -> Dict[str, Any]:
        params = {"KeyId": self.key_id, "KeySpec": self.key_spec}
        if self.encryption_context:
            params["EncryptionContext"] = self.encryption_context
        if self.number_of_bytes:
            params["NumberOfBytes"] = self.number_of_bytes
            params.pop("KeySpec", None)
        return params


@dataclass
class GenerateDataKeyResponse:
    plaintext_key: str
    encrypted_key: str
    key_id: str
    plaintext_key_bytes: Optional[bytes] = field(default=None, repr=False)
    encrypted_key_bytes: Optional[bytes] = field(default=None, repr=False)

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "GenerateDataKeyResponse":
        return cls(
            plaintext_key=base64.b64encode(response["Plaintext"]).decode("utf-8"),
            encrypted_key=base64.b64encode(response["CiphertextBlob"]).decode("utf-8"),
            key_id=response["KeyId"],
            plaintext_key_bytes=response["Plaintext"],
            encrypted_key_bytes=response["CiphertextBlob"],
        )


@dataclass
class SignRequest:
    key_id: str
    message: str
    signing_algorithm: str = SigningAlgorithm.RSASSA_PSS_SHA_256
    message_type: str = MessageType.RAW

    def to_aws_params(self) -> Dict[str, Any]:
        return {
            "KeyId": self.key_id,
            "Message": self.message.encode("utf-8"),
            "SigningAlgorithm": self.signing_algorithm,
            "MessageType": self.message_type,
        }


@dataclass
class SignResponse:
    signature: str
    key_id: str
    signing_algorithm: str
    signature_bytes: Optional[bytes] = field(default=None, repr=False)

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "SignResponse":
        sig_bytes = response["Signature"]
        return cls(
            signature=base64.b64encode(sig_bytes).decode("utf-8"),
            key_id=response["KeyId"],
            signing_algorithm=response.get("SigningAlgorithm", ""),
            signature_bytes=sig_bytes,
        )


@dataclass
class VerifyRequest:
    key_id: str
    message: str
    signature: str
    signing_algorithm: str = SigningAlgorithm.RSASSA_PSS_SHA_256
    message_type: str = MessageType.RAW

    def to_aws_params(self) -> Dict[str, Any]:
        return {
            "KeyId": self.key_id,
            "Message": self.message.encode("utf-8"),
            "Signature": base64.b64decode(self.signature),
            "SigningAlgorithm": self.signing_algorithm,
            "MessageType": self.message_type,
        }


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str

    @classmethod
    def from_aws_response(cls, response: Dict[str, Any]) -> "VerifyResponse":
        return cls(
            signature_valid=response.get("SignatureValid", False),
            key_id=response.get("KeyId", ""),
            signing_algorithm=response.get("SigningAlgorithm", ""),
        )


@dataclass
class EnvelopeEncryptResult:
    encrypted_data_key: str
    ciphertext_blob: str
    key_id: str
    iv: str
    encryption_context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "encrypted_data_key": self.encrypted_data_key,
            "ciphertext_blob": self.ciphertext_blob,
            "key_id": self.key_id,
            "iv": self.iv,
            "encryption_context": self.encryption_context,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EnvelopeEncryptResult":
        return cls(
            encrypted_data_key=data["encrypted_data_key"],
            ciphertext_blob=data["ciphertext_blob"],
            key_id=data["key_id"],
            iv=data["iv"],
            encryption_context=data.get("encryption_context"),
        )


@dataclass
class EnvelopeDecryptRequest:
    encrypted_data_key: str
    ciphertext_blob: str
    key_id: str
    iv: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class KeyUsageEvent:
    key_id: str
    operation: str
    timestamp: str
    success: bool
    algorithm: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class KeyUsageSummary:
    key_id: str
    total_operations: int
    successful_operations: int
    failed_operations: int
    operations_breakdown: Dict[str, int]
    recent_events: List[KeyUsageEvent]
    summary_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "total_operations": self.total_operations,
            "successful_operations": self.successful_operations,
            "failed_operations": self.failed_operations,
            "operations_breakdown": self.operations_breakdown,
            "recent_events": [e.to_dict() for e in self.recent_events],
            "summary_text": self.summary_text,
        }


@dataclass
class SafetyCheckResult:
    is_safe: bool
    categories: Dict[str, float]
    flagged_categories: List[str]
    overall_score: float
    details: str = ""


@dataclass
class EmbeddingResult:
    embedding: List[float]
    model: str
    input_text: str
    usage: Optional[Dict[str, int]] = None


@dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    model: str = ""
