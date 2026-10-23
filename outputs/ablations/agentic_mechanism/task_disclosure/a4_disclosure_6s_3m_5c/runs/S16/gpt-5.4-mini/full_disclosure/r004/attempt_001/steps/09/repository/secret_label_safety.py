import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class SafetyFinding:
    label: str
    unsafe: bool
    reason: str
    source: str


def _normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


def _collect_text_fields(payload: Dict[str, Any]) -> str:
    parts: List[str] = []
    for key in ("label", "labels", "note", "notes", "description", "summary", "comment"):
        if key not in payload:
            continue
        value = payload[key]
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend([str(item) for item in value if item is not None])
    return " \n".join(parts)


def _local_heuristic_check(text: str) -> SafetyFinding:
    suspicious_patterns = {
        "secrets": r"\b(api[_ -]?key|secret|token|password|passwd|private[_ -]?key|credential)\b",
        "exfiltration": r"\b(exfiltrate|dump|leak|steal|bypass|override|ignore policy)\b",
        "unsafe formatting": r"(?i)(begin private key|ssh-rsa|authorization:\s*bearer)",
    }
    lowered = text.lower()
    for reason, pattern in suspicious_patterns.items():
        if re.search(pattern, lowered, flags=re.IGNORECASE):
            return SafetyFinding(label=text[:120], unsafe=True, reason=reason, source="heuristic")
    return SafetyFinding(label=text[:120], unsafe=False, reason="no obvious unsafe text", source="heuristic")


def _openai_safety_check(text: str) -> SafetyFinding:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return _local_heuristic_check(text)

    prompt = (
        "Assess whether the following secret label or notes contain unsafe text, such as passwords, tokens, "
        "API keys, private keys, exfiltration instructions, or other sensitive data. Respond with JSON only "
        "matching keys: unsafe (boolean), reason (string). Text: "
        + text
    )
    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a strict security classifier."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    try:
        parsed = json.loads(content)
        unsafe = bool(parsed.get("unsafe", False))
        reason = str(parsed.get("reason", "")) or ("unsafe" if unsafe else "safe")
    except Exception:
        unsafe = "unsafe" in content.lower()
        reason = content.strip()[:200] or ("unsafe" if unsafe else "safe")
    return SafetyFinding(label=text[:120], unsafe=unsafe, reason=reason, source="openai")


def evaluate_secret_labels_and_notes(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = _collect_text_fields(payload)
    finding = _openai_safety_check(text) if text else SafetyFinding(label="", unsafe=False, reason="empty input", source="heuristic")
    return {
        "unsafe": finding.unsafe,
        "reason": finding.reason,
        "source": finding.source,
        "label_preview": finding.label,
    }


def check_secret_label_safety(label: str, notes: Optional[str] = None) -> Dict[str, Any]:
    payload = {"label": label, "notes": notes or ""}
    return evaluate_secret_labels_and_notes(payload)


__all__ = ["check_secret_label_safety", "evaluate_secret_labels_and_notes", "SafetyFinding"]
