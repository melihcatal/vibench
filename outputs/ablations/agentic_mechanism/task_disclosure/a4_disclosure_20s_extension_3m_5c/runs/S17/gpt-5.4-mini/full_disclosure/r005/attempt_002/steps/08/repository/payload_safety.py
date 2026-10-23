import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class SafetyFinding:
    category: str
    severity: str
    matched_text: str


@dataclass
class SafetyResult:
    safe: bool
    score: float
    findings: List[SafetyFinding]
    provider: str = "openai"
    model: str = OPENAI_MODEL

    def to_dict(self) -> Dict[str, Any]:
        return {
            "safe": self.safe,
            "score": self.score,
            "provider": self.provider,
            "model": self.model,
            "findings": [finding.__dict__ for finding in self.findings],
        }


_DEFAULT_PATTERNS = [
    ("credential", "high", re.compile(r"\b(api[_-]?key|secret|token|password|passwd|private key)\b", re.I)),
    ("payment", "high", re.compile(r"\b(?:\d[ -]*?){13,19}\b")),
    ("malware", "high", re.compile(r"\b(?:rm\s+-rf\s+/|powershell\s+-enc|curl\s+.*\|\s*bash|base64\s+-d)\b", re.I)),
    ("pii", "medium", re.compile(r"\b\d{3}-\d{2}-\d{4}\b|\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
]


def _local_scan(text: str) -> SafetyResult:
    findings: List[SafetyFinding] = []
    score = 0.0
    for category, severity, pattern in _DEFAULT_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(SafetyFinding(category=category, severity=severity, matched_text=match.group(0)))
            score += 0.3 if severity == "high" else 0.15
    score = min(score, 1.0)
    return SafetyResult(safe=score < 0.3, score=score, findings=findings)


def _openai_review(text: str, api_key: str, timeout: int = 30) -> SafetyResult:
    prompt = (
        "Review the following decrypted payload for unsafe content. "
        "Return strict JSON with keys safe(boolean), score(number 0-1), findings(array of objects with category, severity, matched_text). "
        "Unsafe content includes secrets, credentials, malware instructions, exfiltration, or sensitive personal data.\n\n"
        f"PAYLOAD:\n{text}"
    )
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a strict security review assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=timeout,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    data = json.loads(content)
    findings = [SafetyFinding(**item) for item in data.get("findings", [])]
    return SafetyResult(
        safe=bool(data.get("safe", False)),
        score=float(data.get("score", 0.0)),
        findings=findings,
        provider="openai",
        model=OPENAI_MODEL,
    )


def check_decrypted_payload(payload: str, use_provider: bool = True) -> Dict[str, Any]:
    local_result = _local_scan(payload)
    api_key = os.getenv("OPENAI_API_KEY")
    if use_provider and api_key:
        try:
            remote_result = _openai_review(payload, api_key)
            if remote_result.score >= local_result.score:
                return remote_result.to_dict()
        except Exception:
            pass
    return local_result.to_dict()


def summarize_findings(findings: Iterable[Dict[str, Any]]) -> str:
    items = list(findings)
    if not items:
        return "No unsafe content detected."
    return "; ".join(f"{item.get('category')}:{item.get('severity')}" for item in items)


__all__ = ["check_decrypted_payload", "summarize_findings", "SafetyResult", "SafetyFinding"]
