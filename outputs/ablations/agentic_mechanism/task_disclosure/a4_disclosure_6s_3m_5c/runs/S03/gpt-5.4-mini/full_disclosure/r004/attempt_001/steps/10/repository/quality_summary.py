from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence

from openai import OpenAI


@dataclass
class QualityIssue:
    issue_type: str
    severity: str
    description: str
    segment_id: Optional[str] = None
    source_text: Optional[str] = None
    translated_text: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QualitySummary:
    summary: str
    issues: List[QualityIssue] = field(default_factory=list)
    overall_quality: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def _load_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("TRANSLATION_API_KEY")
    if not api_key:
        raise ValueError("Missing API key: set OPENAI_API_KEY or TRANSLATION_API_KEY")
    kwargs: Dict[str, Any] = {"api_key": api_key}
    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        kwargs["base_url"] = base_url
    organization = os.getenv("OPENAI_ORGANIZATION")
    if organization:
        kwargs["organization"] = organization
    project = os.getenv("OPENAI_PROJECT")
    if project:
        kwargs["project"] = project
    return OpenAI(**kwargs)


def _normalize_issue(issue: Mapping[str, Any]) -> QualityIssue:
    return QualityIssue(
        issue_type=str(issue.get("issue_type", "unknown")).strip(),
        severity=str(issue.get("severity", "medium")).strip(),
        description=str(issue.get("description", "")).strip(),
        segment_id=issue.get("segment_id"),
        source_text=issue.get("source_text"),
        translated_text=issue.get("translated_text"),
        metadata=dict(issue.get("metadata", {}) or {}),
    )


def summarize_quality_issues(
    segments: Sequence[Mapping[str, Any]],
    source_language: str,
    target_language: str,
    model: Optional[str] = None,
) -> QualitySummary:
    client = _load_client()
    chosen_model = model or os.getenv("TRANSLATION_MODEL", "gpt-5.4-mini")
    response = client.responses.create(
        model=chosen_model,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a translation quality analyst. Review translated segments for issues such as "
                    "mistranslation, omission, addition, terminology drift, punctuation errors, tone mismatch, "
                    "and untranslated text. Return a concise JSON object with keys summary, overall_quality, and issues. "
                    f"Assess translations from {source_language} to {target_language}."
                ),
            },
            {
                "role": "user",
                "content": {
                    "source_language": source_language,
                    "target_language": target_language,
                    "segments": list(segments),
                },
            },
        ],
        response_format={"type": "json_object"},
    )
    payload = response.output_text or "{}"
    data = {} if not payload.strip() else __import__("json").loads(payload)
    issues = [_normalize_issue(item) for item in data.get("issues", []) or []]
    return QualitySummary(
        summary=str(data.get("summary", "")).strip(),
        issues=issues,
        overall_quality=data.get("overall_quality"),
        metadata={"model": chosen_model},
    )
