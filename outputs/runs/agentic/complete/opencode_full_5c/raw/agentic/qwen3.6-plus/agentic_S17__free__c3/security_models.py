import base64
import hashlib
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class CryptoAction(str, Enum):
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    ENVELOPE_ENCRYPT = "envelope_encrypt"
    ENVELOPE_DECRYPT = "envelope_decrypt"
    SIGN = "sign"
    VERIFY = "verify"


class SigningAlgorithm(str, Enum):
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    RSASSA_PKCS1_V1_5_SHA_384 = "RSASSA_PKCS1_V1_5_SHA_384"
    RSASSA_PKCS1_V1_5_SHA_512 = "RSASSA_PKCS1_V1_5_SHA_512"
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    RSASSA_PSS_SHA_384 = "RSASSA_PSS_SHA_384"
    RSASSA_PSS_SHA_512 = "RSASSA_PSS_SHA_512"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    ECDSA_SHA_384 = "ECDSA_SHA_384"
    ECDSA_SHA_512 = "ECDSA_SHA_512"


class EncryptionAlgorithm(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSAES_OAEP_SHA_1 = "RSAES_OAEP_SHA_1"
    RSAES_OAEP_SHA_256 = "RSAES_OAEP_SHA_256"


@dataclass
class EncryptionRequest:
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    grant_tokens: Optional[List[str]] = None

    def to_provider_payload(self) -> Dict[str, Any]:
        payload = {
            "KeyId": self.key_id,
            "Plaintext": base64.b64encode(self.plaintext.encode("utf-8")),
        }
        if self.encryption_context:
            payload["EncryptionContext"] = self.encryption_context
        if self.grant_tokens:
            payload["GrantTokens"] = self.grant_tokens
        if self.encryption_algorithm != EncryptionAlgorithm.SYMMETRIC_DEFAULT:
            payload["EncryptionAlgorithm"] = self.encryption_algorithm.value
        return payload


@dataclass
class EncryptionResponse:
    ciphertext_blob: str
    key_id: str
    encryption_algorithm: str
    request_id: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def from_provider_response(cls, response: Dict[str, Any]) -> "EncryptionResponse":
        return cls(
            ciphertext_blob=base64.b64encode(response["CiphertextBlob"]).decode(
                "utf-8"
            ),
            key_id=response.get("KeyId", ""),
            encryption_algorithm=response.get(
                "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
            ),
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class DecryptionRequest:
    ciphertext_blob: str
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None

    def to_provider_payload(self) -> Dict[str, Any]:
        payload = {
            "CiphertextBlob": base64.b64decode(self.ciphertext_blob),
        }
        if self.encryption_context:
            payload["EncryptionContext"] = self.encryption_context
        if self.grant_tokens:
            payload["GrantTokens"] = self.grant_tokens
        return payload


@dataclass
class DecryptionResponse:
    plaintext: str
    key_id: str
    encryption_algorithm: str
    request_id: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def from_provider_response(cls, response: Dict[str, Any]) -> "DecryptionResponse":
        return cls(
            plaintext=response["Plaintext"].decode("utf-8"),
            key_id=response.get("KeyId", ""),
            encryption_algorithm=response.get(
                "EncryptionAlgorithm", "SYMMETRIC_DEFAULT"
            ),
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class EnvelopeEncryptionRequest:
    key_id: str
    plaintext: str
    encryption_context: Optional[Dict[str, str]] = None
    data_key_spec: str = "AES_256"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: str
    ciphertext_blob: str
    key_id: str
    request_id: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class SigningRequest:
    key_id: str
    message: str
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256
    message_type: str = "RAW"
    encryption_context: Optional[Dict[str, str]] = None

    def to_provider_payload(self) -> Dict[str, Any]:
        payload = {
            "KeyId": self.key_id,
            "Message": base64.b64encode(self.message.encode("utf-8")),
            "SigningAlgorithm": self.signing_algorithm.value,
            "MessageType": self.message_type,
        }
        if self.encryption_context:
            payload["EncryptionContext"] = self.encryption_context
        return payload


@dataclass
class SigningResponse:
    signature: str
    key_id: str
    signing_algorithm: str
    request_id: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def from_provider_response(cls, response: Dict[str, Any]) -> "SigningResponse":
        return cls(
            signature=base64.b64encode(response["Signature"]).decode("utf-8"),
            key_id=response.get("KeyId", ""),
            signing_algorithm=response.get("SigningAlgorithm", ""),
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class VerificationRequest:
    key_id: str
    message: str
    signature: str
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256
    message_type: str = "RAW"
    encryption_context: Optional[Dict[str, str]] = None

    def to_provider_payload(self) -> Dict[str, Any]:
        payload = {
            "KeyId": self.key_id,
            "Message": base64.b64encode(self.message.encode("utf-8")),
            "Signature": base64.b64decode(self.signature),
            "SigningAlgorithm": self.signing_algorithm.value,
            "MessageType": self.message_type,
        }
        if self.encryption_context:
            payload["EncryptionContext"] = self.encryption_context
        return payload


@dataclass
class VerificationResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str
    request_id: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @classmethod
    def from_provider_response(cls, response: Dict[str, Any]) -> "VerificationResponse":
        return cls(
            signature_valid=response.get("SignatureValid", False),
            key_id=response.get("KeyId", ""),
            signing_algorithm=response.get("SigningAlgorithm", ""),
            request_id=response.get("ResponseMetadata", {}).get("RequestId", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class KeyUsageEvent:
    key_id: str
    action: CryptoAction
    timestamp: str
    request_id: str
    success: bool
    error_message: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class KeyUsageSummary:
    key_id: str
    total_operations: int
    encrypt_count: int
    decrypt_count: int
    sign_count: int
    verify_count: int
    error_count: int
    last_used: str
    events: List[KeyUsageEvent] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["events"] = [e.to_dict() for e in self.events]
        return result


@dataclass
class PayloadSafetyResult:
    payload_hash: str
    is_safe: bool
    findings: List[str]
    risk_level: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditEmbeddingRequest:
    audit_notes: str
    key_id: Optional[str] = None
    operation: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuditEmbeddingResponse:
    embedding: List[float]
    model: str
    audit_notes_hash: str
    key_id: Optional[str] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ComplianceTranslationRequest:
    compliance_notes: str
    target_language: str = "en"
    source_language: str = "auto"
    context: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ComplianceTranslationResponse:
    translated_text: str
    source_language_detected: str
    target_language: str
    model: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_payload(payload: str) -> str:
    return payload.strip()


def compute_payload_hash(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def serialize_response(response_obj) -> str:
    return json.dumps(response_obj.to_dict(), default=str)


def deserialize_request(data: Dict[str, Any], request_class) -> Any:
    return request_class(
        **{k: v for k, v in data.items() if k in request_class.__dataclass_fields__}
    )
