from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Iterable, Mapping

import boto3

from security_client import get_secrets_manager_client
from security_models import normalize_secret_payload


AWS_SECRETS_MANAGER = "aws.secretsmanager"


@dataclass(slots=True)
class SecretLabelSafetyResult:
    secret_id: str
    unsafe: bool
    findings: list[str]
    labels: list[str]
    notes: list[str]
    provider: str = AWS_SECRETS_MANAGER


_UNSAFE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?i)\b(password|passwd|pwd|api[_-]?key|secret|token|private[_-]?key|ssh[_-]?key)\b"), "sensitive credential term"),
    (re.compile(r"(?i)\b(test|dummy|sample|example|placeholder|todo|fixme|hack|temp)\b"), "placeholder or nonproduction marker"),
    (re.compile(r"(?i)\b(unencrypted|plain[- ]?text|clear[- ]?text|hardcoded|embedded)\b"), "unsafe storage indicator"),
    (re.compile(r"(?i)\b(credit card|ssn|social security|bank account)\b"), "high-risk personal data reference"),
)


def _as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _iter_text_fields(payload: Mapping[str, Any], keys: Iterable[str]) -> list[str]:
    texts: list[str] = []
    for key in keys:
        value = payload.get(key)
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            texts.extend(_as_text(item).strip() for item in value if _as_text(item).strip())
        else:
            text = _as_text(value).strip()
            if text:
                texts.append(text)
    return texts


def _scan_text(text: str) -> list[str]:
    findings: list[str] = []
    for pattern, label in _UNSAFE_PATTERNS:
        if pattern.search(text):
            findings.append(label)
    return findings


def _extract_metadata(payload: Mapping[str, Any]) -> tuple[list[str], list[str]]:
    labels = _iter_text_fields(payload, ("labels", "tags", "label", "tag", "name"))
    notes = _iter_text_fields(payload, ("notes", "note", "description", "comments", "comment", "doc", "documentation"))
    return labels, notes


def assess_secret_label_safety(payload: Any, secret_id: str | None = None) -> SecretLabelSafetyResult:
    normalized = normalize_secret_payload(payload)
    labels, notes = _extract_metadata(normalized)
    findings: list[str] = []
    for text in labels + notes:
        findings.extend(_scan_text(text))
    return SecretLabelSafetyResult(
        secret_id=_as_text(secret_id or normalized.get("secret_id") or normalized.get("name") or "").strip(),
        unsafe=bool(findings),
        findings=sorted(set(findings)),
        labels=labels,
        notes=notes,
    )


def fetch_secret_metadata(secret_id: str, version_id: str | None = None) -> Mapping[str, Any]:
    client = get_secrets_manager_client()
    kwargs: dict[str, Any] = {"SecretId": secret_id}
    if version_id:
        kwargs["VersionId"] = version_id
    response = client.describe_secret(**kwargs)
    return normalize_secret_payload(response)


def check_secret_label_safety(secret_id: str, version_id: str | None = None) -> SecretLabelSafetyResult:
    metadata = fetch_secret_metadata(secret_id, version_id=version_id)
    return assess_secret_label_safety(metadata, secret_id=secret_id)


def main() -> None:
    secret_id = os.environ.get("SECRET_ID", "").strip()
    if not secret_id:
        raise SystemExit("SECRET_ID is required")
    version_id = os.environ.get("SECRET_VERSION_ID", "").strip() or None
    result = check_secret_label_safety(secret_id, version_id=version_id)
    print(json.dumps({"secret_id": result.secret_id, "unsafe": result.unsafe, "findings": result.findings, "labels": result.labels, "notes": result.notes, "provider": result.provider}))


if __name__ == "__main__":
    main()
