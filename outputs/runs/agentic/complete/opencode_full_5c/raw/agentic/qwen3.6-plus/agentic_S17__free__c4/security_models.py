import os
import base64
import hashlib
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


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


class KeyUsageType(str, Enum):
    ENCRYPT_DECRYPT = "ENCRYPT_DECRYPT"
    SIGN_VERIFY = "SIGN_VERIFY"
    GENERATE_VERIFY_MAC = "GENERATE_VERIFY_MAC"


class KeySpec(str, Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSA_2048 = "RSA_2048"
    RSA_3072 = "RSA_3072"
    RSA_4096 = "RSA_4096"
    ECC_NIST_P256 = "ECC_NIST_P256"
    ECC_NIST_P384 = "ECC_NIST_P384"
    ECC_NIST_P521 = "ECC_NIST_P521"


@dataclass
class EncryptionRequest:
    plaintext: Union[str, bytes]
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    grant_tokens: Optional[List[str]] = None

    def get_plaintext_bytes(self) -> bytes:
        if isinstance(self.plaintext, str):
            return self.plaintext.encode("utf-8")
        return self.plaintext


@dataclass
class EncryptionResponse:
    ciphertext_blob: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str
    http_metadata: Optional[Dict[str, Any]] = None

    def get_ciphertext_b64(self) -> str:
        return base64.b64encode(self.ciphertext_blob).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ciphertext_blob_b64": self.get_ciphertext_b64(),
            "key_id": self.key_id,
            "encryption_algorithm": self.encryption_algorithm,
            "request_id": self.request_id,
        }


@dataclass
class DecryptionRequest:
    ciphertext_blob: Union[str, bytes]
    key_id: Optional[str] = None
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: Optional[EncryptionAlgorithm] = None
    grant_tokens: Optional[List[str]] = None

    def get_ciphertext_bytes(self) -> bytes:
        if isinstance(self.ciphertext_blob, str):
            return base64.b64decode(self.ciphertext_blob)
        return self.ciphertext_blob


@dataclass
class DecryptionResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str

    def get_plaintext_str(self) -> str:
        return self.plaintext.decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plaintext": self.get_plaintext_str(),
            "key_id": self.key_id,
            "encryption_algorithm": self.encryption_algorithm,
            "request_id": self.request_id,
        }


@dataclass
class EnvelopeEncryptionRequest:
    plaintext: Union[str, bytes]
    key_id: str
    encryption_context: Optional[Dict[str, str]] = None
    data_key_spec: KeySpec = KeySpec.SYMMETRIC_DEFAULT

    def get_plaintext_bytes(self) -> bytes:
        if isinstance(self.plaintext, str):
            return self.plaintext.encode("utf-8")
        return self.plaintext


@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data_key: bytes
    ciphertext: bytes
    key_id: str
    encryption_algorithm: str
    data_key_spec: str
    request_id: str

    def get_encrypted_data_key_b64(self) -> str:
        return base64.b64encode(self.encrypted_data_key).decode("utf-8")

    def get_ciphertext_b64(self) -> str:
        return base64.b64encode(self.ciphertext).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "encrypted_data_key_b64": self.get_encrypted_data_key_b64(),
            "ciphertext_b64": self.get_ciphertext_b64(),
            "key_id": self.key_id,
            "encryption_algorithm": self.encryption_algorithm,
            "data_key_spec": self.data_key_spec,
            "request_id": self.request_id,
        }


@dataclass
class SigningRequest:
    message: Union[str, bytes]
    key_id: str
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256
    message_type: MessageType = MessageType.RAW
    encryption_context: Optional[Dict[str, str]] = None

    def get_message_bytes(self) -> bytes:
        if isinstance(self.message, str):
            return self.message.encode("utf-8")
        return self.message


@dataclass
class SigningResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str
    request_id: str

    def get_signature_b64(self) -> str:
        return base64.b64encode(self.signature).decode("utf-8")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature_b64": self.get_signature_b64(),
            "key_id": self.key_id,
            "signing_algorithm": self.signing_algorithm,
            "request_id": self.request_id,
        }


@dataclass
class VerificationRequest:
    message: Union[str, bytes]
    signature: Union[str, bytes]
    key_id: str
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.ECDSA_SHA_256
    message_type: MessageType = MessageType.RAW
    encryption_context: Optional[Dict[str, str]] = None

    def get_message_bytes(self) -> bytes:
        if isinstance(self.message, str):
            return self.message.encode("utf-8")
        return self.message

    def get_signature_bytes(self) -> bytes:
        if isinstance(self.signature, str):
            return base64.b64decode(self.signature)
        return self.signature


@dataclass
class VerificationResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str
    request_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "signature_valid": self.signature_valid,
            "key_id": self.key_id,
            "signing_algorithm": self.signing_algorithm,
            "request_id": self.request_id,
        }


@dataclass
class KeyMetadata:
    key_id: str
    key_arn: str
    key_state: str
    key_usage: str
    key_spec: str
    creation_date: Optional[datetime] = None
    description: Optional[str] = None
    enabled: bool = True


@dataclass
class KeyUsageEvent:
    event_id: str
    key_id: str
    action: str
    timestamp: datetime
    encryption_context: Optional[Dict[str, str]] = None
    principal: Optional[str] = None
    source_ip: Optional[str] = None


@dataclass
class KeyUsageSummary:
    key_id: str
    key_arn: str
    total_encryptions: int = 0
    total_decryptions: int = 0
    total_signatures: int = 0
    total_verifications: int = 0
    total_generate_data_key: int = 0
    events: List[KeyUsageEvent] = field(default_factory=list)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_id": self.key_id,
            "key_arn": self.key_arn,
            "total_encryptions": self.total_encryptions,
            "total_decryptions": self.total_decryptions,
            "total_signatures": self.total_signatures,
            "total_verifications": self.total_verifications,
            "total_generate_data_key": self.total_generate_data_key,
            "period_start": self.period_start.isoformat()
            if self.period_start
            else None,
            "period_end": self.period_end.isoformat() if self.period_end else None,
            "event_count": len(self.events),
        }


@dataclass
class PayloadSafetyFlag:
    category: str
    severity: str
    description: str
    matched_content: Optional[str] = None


@dataclass
class PayloadSafetyResult:
    payload_hash: str
    is_safe: bool
    flags: List[PayloadSafetyFlag] = field(default_factory=list)
    analysis_timestamp: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "payload_hash": self.payload_hash,
            "is_safe": self.is_safe,
            "flags": [
                {
                    "category": f.category,
                    "severity": f.severity,
                    "description": f.description,
                    "matched_content": f.matched_content,
                }
                for f in self.flags
            ],
            "analysis_timestamp": self.analysis_timestamp.isoformat()
            if self.analysis_timestamp
            else None,
        }


@dataclass
class AuditEmbedding:
    text: str
    embedding: List[float]
    model: str
    metadata: Optional[Dict[str, Any]] = None
    embedding_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "embedding_id": self.embedding_id,
            "text": self.text,
            "model": self.model,
            "embedding": self.embedding,
            "metadata": self.metadata,
        }


@dataclass
class ComplianceNote:
    original_text: str
    source_language: str
    target_language: str
    translated_text: str
    model: str
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "translated_text": self.translated_text,
            "model": self.model,
            "metadata": self.metadata,
        }


def normalize_payload(payload: Union[str, bytes]) -> bytes:
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return payload


def normalize_ciphertext(ciphertext: Union[str, bytes]) -> bytes:
    if isinstance(ciphertext, str):
        return base64.b64decode(ciphertext)
    return ciphertext


def compute_payload_hash(payload: Union[str, bytes]) -> str:
    payload_bytes = normalize_payload(payload)
    return hashlib.sha256(payload_bytes).hexdigest()


def serialize_event(event: KeyUsageEvent) -> Dict[str, Any]:
    return {
        "event_id": event.event_id,
        "key_id": event.key_id,
        "action": event.action,
        "timestamp": event.timestamp.isoformat() if event.timestamp else None,
        "encryption_context": event.encryption_context,
        "principal": event.principal,
        "source_ip": event.source_ip,
    }


def parse_kms_response_metadata(http_response) -> Dict[str, Any]:
    metadata = {}
    if hasattr(http_response, "get"):
        metadata["http_status_code"] = http_response.get("ResponseMetadata", {}).get(
            "HTTPStatusCode"
        )
        metadata["request_id"] = http_response.get("ResponseMetadata", {}).get(
            "RequestId"
        )
        metadata["headers"] = dict(
            http_response.get("ResponseMetadata", {}).get("HTTPHeaders", {})
        )
    return metadata
