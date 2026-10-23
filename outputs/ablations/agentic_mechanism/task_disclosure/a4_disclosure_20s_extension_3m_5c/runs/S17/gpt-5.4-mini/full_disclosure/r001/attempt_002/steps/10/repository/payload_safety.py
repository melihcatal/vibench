import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
OPENAI_API_URL = "https://api.openai.com/v1/moderations"


@dataclass
class SafetyResult:
    unsafe: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    flagged_text: Optional[str]
    provider: str = "openai"
    model: str = OPENAI_MODERATION_MODEL


def _normalize_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, bytes):
        return payload.decode("utf-8", errors="replace")
    if isinstance(payload, str):
        return payload
    if isinstance(payload, dict):
        for key in ("text", "payload", "content", "decrypted_text"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
        return str(payload)
    return str(payload)


def _fallback_local_checks(text: str) -> SafetyResult:
    patterns = {
        "self_harm": re.compile(r"\b(suicide|kill myself|self-harm|harm myself)\b", re.I),
        "violence": re.compile(r"\b(bomb|explosive|shoot|stab|murder)\b", re.I),
        "illicit": re.compile(r"\b(malware|ransomware|phishing|credential stuffing)\b", re.I),
        "privacy": re.compile(r"\b(ssn|social security number|credit card|api key|private key)\b", re.I),
    }
    categories = {name: bool(pattern.search(text)) for name, pattern in patterns.items()}
    unsafe = any(categories.values())
    scores = {name: 1.0 if flagged else 0.0 for name, flagged in categories.items()}
    return SafetyResult(unsafe=unsafe, categories=categories, category_scores=scores, flagged_text=text if unsafe else None)


def _openai_moderate(text: str, api_key: str) -> SafetyResult:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    result = (data.get("results") or [{}])[0]
    categories = result.get("categories") or {}
    scores = result.get("category_scores") or {}
    unsafe = bool(result.get("flagged"))
    return SafetyResult(
        unsafe=unsafe,
        categories={str(k): bool(v) for k, v in categories.items()},
        category_scores={str(k): float(v) for k, v in scores.items()},
        flagged_text=text if unsafe else None,
    )


def check_decrypted_payload(payload: Any, api_key: Optional[str] = None) -> SafetyResult:
    text = _normalize_text(payload)
    if not text.strip():
        return SafetyResult(unsafe=False, categories={}, category_scores={}, flagged_text=None)
    key = api_key or os.getenv("OPENAI_API_KEY")
    if key:
        try:
            return _openai_moderate(text, key)
        except Exception:
            pass
    return _fallback_local_checks(text)


def payload_is_safe(payload: Any, api_key: Optional[str] = None) -> bool:
    return not check_decrypted_payload(payload, api_key=api_key).unsafe
