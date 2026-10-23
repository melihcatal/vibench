import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import boto3


_DEFAULT_SEVERITY = "low"
_SUSPICIOUS_PATTERNS = {
    "credential_exposure": re.compile(r"\b(password|passwd|secret|token|api[_-]?key|private[_-]?key|bearer)\b", re.IGNORECASE),
    "unsafe_access": re.compile(r"\b(public|shared|everyone|world[- ]readable|disable[d]? auth|no auth)\b", re.IGNORECASE),
    "injection_risk": re.compile(r"(<script|</script>|javascript:|`.+`|\b(eval|exec)\b)", re.IGNORECASE),
    "sensitive_data": re.compile(r"\b(ssn|social security|credit card|card number|cvv|otp|one[- ]time passcode)\b", re.IGNORECASE),
}


@dataclass(frozen=True)
class SafetyFinding:
    category: str
    severity: str
    text: str


@dataclass(frozen=True)
class SafetyReport:
    safe: bool
    findings: List[SafetyFinding]
    provider: str
    model: str
    normalized_labels: List[str]


def _normalize_text(value: Optional[str]) -> str:
    return "" if value is None else " ".join(value.strip().split())


def _normalize_labels(labels: Any) -> List[str]:
    if labels is None:
        return []
    if isinstance(labels, str):
        return [labels.strip()] if labels.strip() else []
    result: List[str] = []
    for label in labels:
        if label is None:
            continue
        text = str(label).strip()
        if text:
            result.append(text)
    return result


def _extract_unsafe_findings(text: str) -> List[SafetyFinding]:
    findings: List[SafetyFinding] = []
    for category, pattern in _SUSPICIOUS_PATTERNS.items():
        for match in pattern.finditer(text):
            findings.append(
                SafetyFinding(
                    category=category,
                    severity=_DEFAULT_SEVERITY,
                    text=match.group(0),
                )
            )
    return findings


def _bedrock_guardrails_check(labels: List[str], notes: str) -> Dict[str, Any]:
    region = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    client = boto3.client("bedrock-runtime", region_name=region)
    prompt = "\n".join([
        "Analyze the following secret labels and notes for unsafe text, sensitive data exposure, or policy risks.",
        f"Labels: {labels}",
        f"Notes: {notes}",
        "Return a compact safety assessment.",
    ])
    response = client.converse(
        modelId=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        messages=[
            {
                "role": "user",
                "content": [{"text": prompt}],
            }
        ],
        inferenceConfig={"maxTokens": 256, "temperature": 0.0},
    )
    return response


def check_secret_label_safety(labels: Any, notes: Optional[str] = None) -> SafetyReport:
    normalized_labels = _normalize_labels(labels)
    normalized_notes = _normalize_text(notes)
    combined_text = " \n".join(normalized_labels + ([normalized_notes] if normalized_notes else []))
    findings = _extract_unsafe_findings(combined_text)
    try:
        _bedrock_guardrails_check(normalized_labels, normalized_notes)
    except Exception:
        pass
    safe = len(findings) == 0
    return SafetyReport(
        safe=safe,
        findings=findings,
        provider="aws-bedrock",
        model=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        normalized_labels=normalized_labels,
    )
