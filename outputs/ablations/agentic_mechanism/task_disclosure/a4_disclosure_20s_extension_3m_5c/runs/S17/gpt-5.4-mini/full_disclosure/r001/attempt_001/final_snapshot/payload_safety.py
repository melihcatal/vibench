from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

from openai import OpenAI


@dataclass(frozen=True)
class SafetyFinding:
    is_safe: bool
    risk_level: str
    categories: Dict[str, str]
    explanation: str
    provider: str = "openai"
    model: str = "gpt-5.4-mini"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "risk_level": self.risk_level,
            "categories": dict(self.categories),
            "explanation": self.explanation,
            "provider": self.provider,
            "model": self.model,
        }


def _build_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _normalize_text(payload: Any) -> str:
    if payload is None:
        return ""
    if isinstance(payload, bytes):
        return payload.decode("utf-8", errors="replace")
    return str(payload)


def _local_heuristic(text: str) -> SafetyFinding:
    lowered = text.lower()
    categories: Dict[str, str] = {}
    if any(token in lowered for token in ("password", "api key", "secret", "private key", "token")):
        categories["credential_exposure"] = "possible"
    if any(token in lowered for token in ("ssn", "social security", "credit card", "cvv")):
        categories["sensitive_personal_data"] = "possible"
    if any(token in lowered for token in ("malware", "ransomware", "exploit", "phishing")):
        categories["malicious_content"] = "possible"
    if any(token in lowered for token in ("self-harm", "suicide", "bomb", "weapon")):
        categories["harmful_content"] = "possible"
    is_safe = not categories
    risk_level = "low" if is_safe else "high"
    explanation = "No obvious unsafe content detected." if is_safe else "Potentially unsafe content detected by heuristic scan."
    return SafetyFinding(is_safe=is_safe, risk_level=risk_level, categories=categories, explanation=explanation)


def check_payload_safety(payload: Any, *, use_provider: bool = True) -> Mapping[str, Any]:
    text = _normalize_text(payload)
    heuristic = _local_heuristic(text)
    if not use_provider or not text:
        return heuristic.to_dict()

    client = _build_client()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Assess decrypted text payloads for unsafe content. "
                    "Return a compact JSON object with keys is_safe, risk_level, categories, explanation."
                ),
            },
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    content = getattr(response, "output_text", None) or ""
    if not content:
        return heuristic.to_dict()
    return {
        "provider": "openai",
        "model": "gpt-5.4-mini",
        "analysis": content,
        **heuristic.to_dict(),
    }
