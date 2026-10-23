from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Iterable

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL_HINT = "omni-moderation-latest"


@dataclass(frozen=True)
class LabelSafetyFinding:
    field: str
    unsafe: bool
    categories: tuple[str, ...]
    flagged: bool
    severity: str
    explanation: str


@dataclass(frozen=True)
class LabelSafetyReport:
    label: str
    notes: str
    unsafe: bool
    findings: tuple[LabelSafetyFinding, ...]


def _first_env(*names: str) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _chunks(text: str, size: int = 4000) -> Iterable[str]:
    if not text:
        return ()
    return (text[i : i + size] for i in range(0, len(text), size))


def _moderate_text(text: str, api_key: str, timeout: float | None = None) -> dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL_HINT, "input": text},
        timeout=timeout or 30,
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results") or []
    return results[0] if results else {"flagged": False, "categories": {}, "category_scores": {}}


def _severity_from_scores(scores: dict[str, Any]) -> str:
    if not scores:
        return "low"
    max_score = max((float(v) for v in scores.values() if isinstance(v, (int, float))), default=0.0)
    if max_score >= 0.9:
        return "critical"
    if max_score >= 0.7:
        return "high"
    if max_score >= 0.4:
        return "medium"
    return "low"


def _build_finding(field: str, text: str, result: dict[str, Any]) -> LabelSafetyFinding:
    categories = tuple(sorted(name for name, enabled in (result.get("categories") or {}).items() if enabled))
    scores = result.get("category_scores") or {}
    explanation = f"OpenAI moderation flagged={bool(result.get('flagged'))}"
    if categories:
        explanation = f"{explanation}; categories={', '.join(categories)}"
    return LabelSafetyFinding(
        field=field,
        unsafe=bool(result.get("flagged")),
        categories=categories,
        flagged=bool(result.get("flagged")),
        severity=_severity_from_scores(scores),
        explanation=explanation,
    )


def check_secret_label_safety(label: str, notes: str, api_key: str | None = None, timeout: float | None = None) -> LabelSafetyReport:
    resolved_api_key = api_key or _first_env("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError("Missing OpenAI API key; set OPENAI_API_KEY")
    label_result = _moderate_text(label, resolved_api_key, timeout=timeout)
    note_findings = []
    note_unsafe = False
    for chunk in _chunks(notes):
        result = _moderate_text(chunk, resolved_api_key, timeout=timeout)
        note_findings.append(_build_finding("notes", chunk, result))
        note_unsafe = note_unsafe or bool(result.get("flagged"))
    label_finding = _build_finding("label", label, label_result)
    unsafe = label_finding.unsafe or note_unsafe
    findings = (label_finding, *note_findings)
    return LabelSafetyReport(label=label, notes=notes, unsafe=unsafe, findings=findings)


def check_secret_label_safety_from_json(payload: str, api_key: str | None = None, timeout: float | None = None) -> str:
    data = json.loads(payload)
    report = check_secret_label_safety(
        label=str(data.get("label", "")),
        notes=str(data.get("notes", "")),
        api_key=api_key,
        timeout=timeout,
    )
    return json.dumps(
        {
            "label": report.label,
            "notes": report.notes,
            "unsafe": report.unsafe,
            "findings": [finding.__dict__ for finding in report.findings],
        },
        ensure_ascii=False,
    )
