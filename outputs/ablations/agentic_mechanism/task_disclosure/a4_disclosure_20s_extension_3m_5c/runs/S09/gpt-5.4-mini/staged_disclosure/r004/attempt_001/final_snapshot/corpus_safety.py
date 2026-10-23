import os
import re
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


class CorpusSafetyError(ValueError):
    pass


def _auth_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise CorpusSafetyError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _call_openai_moderation(text: str) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers=_auth_headers(),
        json={"model": OPENAI_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def _extract_flagged_categories(payload: Dict[str, Any]) -> List[str]:
    results = payload.get("results") or []
    if not results:
        return []
    categories = results[0].get("categories") or {}
    return [name for name, flagged in categories.items() if flagged]


def _looks_like_secret(text: str) -> Optional[str]:
    patterns = {
        "api_key": r"(?i)\bapi[_-]?key\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",
        "private_key": r"-----BEGIN [A-Z ]+PRIVATE KEY-----",
        "token": r"(?i)\b(bearer\s+)?[A-Za-z0-9_\-]{24,}\.[A-Za-z0-9_\-]{24,}\.[A-Za-z0-9_\-]{24,}\b",
    }
    for label, pattern in patterns.items():
        if re.search(pattern, text):
            return label
    return None


def check_corpus_text(text: str) -> Dict[str, Any]:
    if not isinstance(text, str) or not text.strip():
        raise CorpusSafetyError("text must be a non-empty string")

    secret_type = _looks_like_secret(text)
    if secret_type:
        return {"safe": False, "reason": f"possible_{secret_type}", "provider": "openai"}

    moderation = _call_openai_moderation(text)
    flagged_categories = _extract_flagged_categories(moderation)
    safe = not flagged_categories
    return {
        "safe": safe,
        "reason": None if safe else "moderation_flagged",
        "flagged_categories": flagged_categories,
        "provider": "openai",
        "model": OPENAI_MODEL,
    }
