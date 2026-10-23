import os
import base64
import json
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from enum import Enum


class CryptoOperation(Enum):
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"
    SIGN = "sign"
    VERIFY = "verify"
    GENERATE_DATA_KEY = "generate_data_key"
    RE_ENCRYPT = "re_encrypt"


class KeySpec(Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSA_2048 = "RSA_2048"
    RSA_3072 = "RSA_3072"
    RSA_4096 = "RSA_4096"
    ECC_NIST_P256 = "ECC_NIST_P256"
    ECC_NIST_P384 = "ECC_NIST_P384"


class EncryptionAlgorithm(Enum):
    SYMMETRIC_DEFAULT = "SYMMETRIC_DEFAULT"
    RSAES_OAEP_SHA_1 = "RSAES_OAEP_SHA_1"
    RSAES_OAEP_SHA_256 = "RSAES_OAEP_SHA_256"


class SigningAlgorithm(Enum):
    RSASSA_PSS_SHA_256 = "RSASSA_PSS_SHA_256"
    RSASSA_PSS_SHA_384 = "RSASSA_PSS_SHA_384"
    RSASSA_PSS_SHA_512 = "RSASSA_PSS_SHA_512"
    RSASSA_PKCS1_V1_5_SHA_256 = "RSASSA_PKCS1_V1_5_SHA_256"
    ECDSA_SHA_256 = "ECDSA_SHA_256"
    ECDSA_SHA_384 = "ECDSA_SHA_384"


class MessageType(Enum):
    RAW = "RAW"
    DIGEST = "DIGEST"


@dataclass
class EncryptRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    grant_tokens: Optional[List[str]] = None


@dataclass
class DecryptRequest:
    ciphertext_blob: bytes
    encryption_context: Optional[Dict[str, str]] = None
    encryption_algorithm: EncryptionAlgorithm = EncryptionAlgorithm.SYMMETRIC_DEFAULT
    grant_tokens: Optional[List[str]] = None
    key_id: Optional[str] = None


@dataclass
class GenerateDataKeyRequest:
    key_id: str
    key_spec: Optional[str] = None
    number_of_bytes: Optional[int] = None
    encryption_context: Optional[Dict[str, str]] = None
    grant_tokens: Optional[List[str]] = None


@dataclass
class SignRequest:
    key_id: str
    message: bytes
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256
    message_type: MessageType = MessageType.RAW


@dataclass
class VerifyRequest:
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: SigningAlgorithm = SigningAlgorithm.RSASSA_PSS_SHA_256
    message_type: MessageType = MessageType.RAW


@dataclass
class EncryptResponse:
    ciphertext_blob: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class DecryptResponse:
    plaintext: bytes
    key_id: str
    encryption_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class GenerateDataKeyResponse:
    plaintext_key: bytes
    encrypted_key: bytes
    key_id: str
    request_id: str
    http_status_code: int


@dataclass
class SignResponse:
    signature: bytes
    key_id: str
    signing_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class VerifyResponse:
    signature_valid: bool
    key_id: str
    signing_algorithm: str
    request_id: str
    http_status_code: int


@dataclass
class KeyUsageEvent:
    key_id: str
    operation: str
    timestamp: str
    encryption_context: Optional[Dict[str, str]] = None
    success: bool = True
    error_message: Optional[str] = None


@dataclass
class KeyUsageSummary:
    key_id: str
    total_operations: int = 0
    encrypt_count: int = 0
    decrypt_count: int = 0
    sign_count: int = 0
    verify_count: int = 0
    generate_data_key_count: int = 0
    failed_operations: int = 0
    events: List[KeyUsageEvent] = field(default_factory=list)


@dataclass
class EnvelopeEncryptionResult:
    encrypted_data_key: bytes
    encrypted_payload: bytes
    key_id: str
    algorithm: str
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class EnvelopeDecryptionResult:
    plaintext: bytes
    key_id: str


@dataclass
class AuditNoteEmbedding:
    note_text: str
    embedding: List[float]
    model: str
    timestamp: str
    key_id: Optional[str] = None


@dataclass
class ComplianceTranslation:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    model: str
    key_id: Optional[str] = None


@dataclass
class PayloadSafetyResult:
    payload: str
    is_safe: bool
    safety_categories: Dict[str, str]
    flagged_content: List[str]
    model: str


def normalize_payload_to_bytes(payload: Any) -> bytes:
    if isinstance(payload, bytes):
        return payload
    if isinstance(payload, str):
        return payload.encode("utf-8")
    if isinstance(payload, dict):
        return json.dumps(payload, sort_keys=True).encode("utf-8")
    if isinstance(payload, (list, tuple)):
        return json.dumps(payload, sort_keys=True).encode("utf-8")
    return str(payload).encode("utf-8")


def encode_ciphertext_blob(blob: bytes) -> str:
    return base64.b64encode(blob).decode("utf-8")


def decode_ciphertext_blob(encoded: str) -> bytes:
    return base64.b64decode(encoded)


def response_to_dict(response_obj) -> Dict[str, Any]:
    result = {}
    for k, v in asdict(response_obj).items():
        if isinstance(v, bytes):
            result[k] = encode_ciphertext_blob(v)
        elif isinstance(v, Enum):
            result[k] = v.value
        else:
            result[k] = v
    return result


def dict_to_encrypt_response(data: Dict[str, Any]) -> EncryptResponse:
    return EncryptResponse(
        ciphertext_blob=decode_ciphertext_blob(data["ciphertext_blob"]),
        key_id=data["key_id"],
        encryption_algorithm=data.get("encryption_algorithm", "SYMMETRIC_DEFAULT"),
        request_id=data.get("request_id", ""),
        http_status_code=data.get("http_status_code", 200),
    )


def dict_to_decrypt_response(data: Dict[str, Any]) -> DecryptResponse:
    return DecryptResponse(
        plaintext=decode_ciphertext_blob(data["plaintext"]),
        key_id=data["key_id"],
        encryption_algorithm=data.get("encryption_algorithm", "SYMMETRIC_DEFAULT"),
        request_id=data.get("request_id", ""),
        http_status_code=data.get("http_status_code", 200),
    )


def dict_to_generate_data_key_response(data: Dict[str, Any]) -> GenerateDataKeyResponse:
    return GenerateDataKeyResponse(
        plaintext_key=decode_ciphertext_blob(data["plaintext_key"]),
        encrypted_key=decode_ciphertext_blob(data["encrypted_key"]),
        key_id=data["key_id"],
        request_id=data.get("request_id", ""),
        http_status_code=data.get("http_status_code", 200),
    )


def dict_to_sign_response(data: Dict[str, Any]) -> SignResponse:
    return SignResponse(
        signature=decode_ciphertext_blob(data["signature"]),
        key_id=data["key_id"],
        signing_algorithm=data.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
        request_id=data.get("request_id", ""),
        http_status_code=data.get("http_status_code", 200),
    )


def dict_to_verify_response(data: Dict[str, Any]) -> VerifyResponse:
    return VerifyResponse(
        signature_valid=data["signature_valid"],
        key_id=data["key_id"],
        signing_algorithm=data.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
        request_id=data.get("request_id", ""),
        http_status_code=data.get("http_status_code", 200),
    )
