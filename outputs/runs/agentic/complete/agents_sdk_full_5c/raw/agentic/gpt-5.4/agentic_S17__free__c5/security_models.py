from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import base64
import json


def b64encode_str(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")


def b64decode_str(data: str) -> bytes:
    return base64.b64decode(data.encode("utf-8"))


@dataclass
class EncryptRequest:
    plaintext: str
    key_id: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EncryptResponse:
    key_id: str
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptRequest:
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class DecryptResponse:
    key_id: Optional[str]
    plaintext: str


@dataclass
class EnvelopeEncryptRequest:
    plaintext: str
    key_id: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class EnvelopeEncryptResponse:
    key_id: str
    encrypted_data_key_b64: str
    nonce_b64: str
    ciphertext_b64: str
    encryption_context: Dict[str, str] = field(default_factory=dict)


@dataclass
class SignVerifyRequest:
    key_id: str
    message: str
    action: str = "sign"
    signature_b64: Optional[str] = None
    signing_algorithm: str = "RSASSA_PSS_SHA_256"
    message_type: str = "RAW"


@dataclass
class SignVerifyResponse:
    action: str
    key_id: str
    signature_b64: Optional[str] = None
    verified: Optional[bool] = None
    signing_algorithm: Optional[str] = None


@dataclass
class UsageSummary:
    total_events: int
    actions: Dict[str, int]
    recent_key_arns: List[str]


@dataclass
class SafetyAssessment:
    safe: bool
    categories: List[str]
    provider: str
    raw: Dict[str, Any]


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]


@dataclass
class TranslationResult:
    provider: str
    model: str
    translated_text: str


def json_dumps(data: Dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True)


def normalize_cloudtrail_events(events: List[Dict[str, Any]]) -> UsageSummary:
    actions: Dict[str, int] = {}
    key_arns: List[str] = []
    for event in events:
        name = event.get("EventName") or event.get("eventName") or "Unknown"
        actions[name] = actions.get(name, 0) + 1
        resources = event.get("Resources") or event.get("resources") or []
        for resource in resources:
            arn = resource.get("ResourceName") or resource.get("ARN") or resource.get("resourceName")
            if arn and arn not in key_arns:
                key_arns.append(arn)
    return UsageSummary(total_events=len(events), actions=actions, recent_key_arns=key_arns[:10])
