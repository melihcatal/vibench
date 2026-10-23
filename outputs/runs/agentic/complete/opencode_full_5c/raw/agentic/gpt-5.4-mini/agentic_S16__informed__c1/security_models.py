from dataclasses import dataclass
import json


@dataclass
class SecretRequest:
    secret_name: str
    version_id: str | None = None
    version_stage: str | None = None


@dataclass
class RotationSummaryRequest:
    notes: str


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class EmbeddingRequest:
    text: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str


def normalize_secret_value(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value or ''


def parse_json_payload(value):
    raw = normalize_secret_value(value)
    return json.loads(raw) if raw else {}


def normalize_text(value):
    return normalize_secret_value(value).strip()
