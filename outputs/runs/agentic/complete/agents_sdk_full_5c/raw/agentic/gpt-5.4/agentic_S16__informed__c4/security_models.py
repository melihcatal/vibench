from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional
import json


@dataclass
class SecretFetchRequest:
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class SecretPayload:
    secret_id: str
    version_id: str
    value: str
    created_date: Optional[datetime] = None
    stages: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "version_id": self.version_id,
            "value": self.value,
            "created_date": self.created_date.isoformat() if self.created_date else None,
            "stages": list(self.stages),
        }


@dataclass
class RotationSummary:
    secret_id: str
    version_id: str
    stages: List[str]
    created_date: Optional[datetime]
    status: str
    recommendation: str


@dataclass
class SafetyFinding:
    text: str
    unsafe: bool
    scores: Dict[str, float]
    flagged_attributes: List[str]


@dataclass
class EmbeddingResult:
    model: str
    dimensions: int
    vector: List[float]


@dataclass
class TranslationResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str


@dataclass
class SummaryResult:
    model: str
    summary: str


def _parse_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        try:
            cleaned = value.replace("Z", "+00:00")
            dt = datetime.fromisoformat(cleaned)
            return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return None


def normalize_secret_value(secret_id: str, response: Mapping[str, Any]) -> SecretPayload:
    version_id = str(response.get("VersionId") or "")
    secret_string = response.get("SecretString")
    if secret_string is None:
        binary_payload = response.get("SecretBinary") or b""
        if isinstance(binary_payload, bytes):
            secret_string = binary_payload.decode("utf-8")
        else:
            secret_string = str(binary_payload)
    created = _parse_datetime(response.get("CreatedDate"))
    stages = [str(item) for item in response.get("VersionStages", [])]
    return SecretPayload(
        secret_id=secret_id,
        version_id=version_id,
        value=str(secret_string),
        created_date=created,
        stages=stages,
    )


def parse_json_secret_value(secret_payload: SecretPayload) -> Dict[str, Any]:
    parsed = json.loads(secret_payload.value)
    if not isinstance(parsed, dict):
        raise ValueError("Secret value is not a JSON object")
    return parsed


def summarize_rotation(secret_payload: SecretPayload, now: Optional[datetime] = None) -> RotationSummary:
    current_time = now or datetime.now(timezone.utc)
    created = secret_payload.created_date
    age_days: Optional[float] = None
    if created is not None:
        age_days = (current_time - created).total_seconds() / 86400.0

    stages = set(secret_payload.stages)
    if "AWSCURRENT" in stages:
        status = "current"
        recommendation = "No immediate action required."
        if age_days is not None and age_days > 90:
            recommendation = "Current version is older than 90 days; schedule rotation soon."
    elif "AWSPENDING" in stages:
        status = "pending"
        recommendation = "Finish validation and promote pending version when ready."
    elif "AWSPREVIOUS" in stages:
        status = "previous"
        recommendation = "Previous version retained; verify rollback policy and retirement window."
    else:
        status = "untracked"
        recommendation = "Version stage is not one of the standard AWS rotation labels."

    return RotationSummary(
        secret_id=secret_payload.secret_id,
        version_id=secret_payload.version_id,
        stages=secret_payload.stages,
        created_date=created,
        status=status,
        recommendation=recommendation,
    )


def join_text_fields(values: Iterable[Optional[str]]) -> str:
    return "\n".join(part.strip() for part in values if part and part.strip())
