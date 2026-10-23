import os
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from safety_models import SafetyBatchDecision, SafetyDecision, normalize_messages, normalize_text


def get_google_client() -> Any:
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY is required")
    genai.configure(api_key=api_key)
    return genai


def get_model_name() -> str:
    return os.environ.get("GOOGLE_SAFETY_MODEL", "gemini-2.0-flash")


def get_threshold(default: float = 0.5) -> float:
    return float(os.environ.get("SAFETY_THRESHOLD", str(default)))


def build_prompt(text: str) -> str:
    return f"Assess the following user text for unsafe, abusive, hateful, sexual, or policy-violating content. Return concise JSON with fields allowed and categories. Text: {text}"


def parse_categories(payload: Dict[str, Any]) -> Dict[str, float]:
    categories = payload.get("categories") or {}
    result: Dict[str, float] = {}
    for key, value in categories.items():
        try:
            result[str(key)] = float(value)
        except Exception:
            continue
    return result


def make_decision(allowed: bool, categories: Dict[str, float], raw: Optional[Dict[str, Any]] = None) -> SafetyDecision:
    return SafetyDecision(allowed=allowed, categories=categories, raw=raw)


def make_batch_decision(decisions: List[SafetyDecision]) -> SafetyBatchDecision:
    return SafetyBatchDecision(decisions=decisions)
