from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union

from google.cloud import aiplatform_v1


_OPENAI_MODEL = "gemini-1.5-pro"


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (bytes, bytearray, memoryview)):
        try:
            return bytes(value).decode("utf-8")
        except Exception:
            return ""
    return str(value)


def _normalize_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Sequence):
        out: List[str] = []
        for item in value:
            text = _coerce_text(item).strip()
            if text:
                out.append(text)
        return out
    return []


@dataclass(frozen=True)
class SafetyFinding:
    category: str
    detail: str
    severity: str = "medium"

    def normalized(self) -> Dict[str, str]:
        return {"category": self.category, "detail": self.detail, "severity": self.severity}


@dataclass(frozen=True)
class SafetyResult:
    safe: bool
    findings: List[SafetyFinding] = field(default_factory=list)
    provider: str = "google.vertex_ai"
    model: str = _OPENAI_MODEL
    summary: str = ""

    def normalized(self) -> Dict[str, Any]:
        return {
            "safe": self.safe,
            "findings": [finding.normalized() for finding in self.findings],
            "provider": self.provider,
            "model": self.model,
            "summary": self.summary,
        }


_DANGEROUS_PATTERNS = [
    (re.compile(r"\b(password|passwd|api[_-]?key|secret|token)\b", re.I), "credential exposure"),
    (re.compile(r"\b(ssn|social security number|credit card|cvv)\b", re.I), "sensitive personal data"),
    (re.compile(r"\b(drop\s+table|delete\s+from|rm\s+-rf|shutdown\b|format\s+c:)\b", re.I), "destructive command"),
    (re.compile(r"\b(exploit|malware|ransomware|payload|shellcode)\b", re.I), "malicious content"),
    (re.compile(r"\b(?:BEGIN\s+(?:RSA|OPENSSH|EC|DSA)?\s*PRIVATE\s+KEY|PRIVATE\s+KEY)\b", re.I), "private key material"),
]


def _local_findings(text: str) -> List[SafetyFinding]:
    findings: List[SafetyFinding] = []
    for pattern, category in _DANGEROUS_PATTERNS:
        if pattern.search(text):
            findings.append(SafetyFinding(category=category, detail=f"Matched pattern for {category}", severity="high"))
    if len(text) > 200_000:
        findings.append(SafetyFinding(category="oversized payload", detail="Payload is unusually large", severity="low"))
    return findings


def _vertex_ai_safety_review(text: str) -> Optional[SafetyResult]:
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("VERTEX_AI_PROJECT")
    location = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    if not project_id:
        return None
    client = aiplatform_v1.PredictionServiceClient()
    endpoint = os.getenv("VERTEX_AI_SAFETY_ENDPOINT")
    if not endpoint:
        return None
    instance = {"content": text, "task": "payload_safety_review", "model": _OPENAI_MODEL}
    response = client.predict(endpoint=endpoint, instances=[instance], parameters={"model": _OPENAI_MODEL, "location": location})
    predictions = getattr(response, "predictions", None) or []
    findings: List[SafetyFinding] = []
    safe = True
    summary = ""
    for prediction in predictions:
        if isinstance(prediction, Mapping):
            safe = safe and bool(prediction.get("safe", True))
            summary = _coerce_text(prediction.get("summary") or summary)
            for item in _normalize_list(prediction.get("findings")):
                findings.append(SafetyFinding(category="vertex_ai", detail=item, severity="medium"))
    return SafetyResult(safe=safe and not findings, findings=findings, provider="google.vertex_ai", model=_OPENAI_MODEL, summary=summary)


def check_payload_safety(payload: Union[str, bytes, bytearray, memoryview, Mapping[str, Any], Sequence[Any]]) -> SafetyResult:
    if isinstance(payload, Mapping):
        text = _coerce_text(payload.get("plaintext") or payload.get("text") or payload.get("value") or "")
    elif isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray, memoryview)):
        text = "\n".join(_coerce_text(item) for item in payload)
    else:
        text = _coerce_text(payload)
    findings = _local_findings(text)
    review = _vertex_ai_safety_review(text)
    if review is not None:
        combined_findings = findings + review.findings
        return SafetyResult(safe=review.safe and not combined_findings, findings=combined_findings, provider=review.provider, model=review.model, summary=review.summary)
    return SafetyResult(safe=not findings, findings=findings, provider="google.vertex_ai", model=_OPENAI_MODEL, summary="local heuristic review")
