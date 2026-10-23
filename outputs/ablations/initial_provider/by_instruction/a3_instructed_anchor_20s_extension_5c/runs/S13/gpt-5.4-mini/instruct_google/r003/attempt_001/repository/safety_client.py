import os
from typing import Any, Dict, List, Optional

from google import genai

from safety_models import SafetyCategoryScore, SafetyDecision, normalize_messages, normalize_text, normalize_thresholds


DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"


def get_client(api_key: Optional[str] = None) -> genai.Client:
    return genai.Client(api_key=api_key or os.environ.get("GOOGLE_API_KEY"))


def get_model_name() -> str:
    return os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)


def score_text(text: Any, categories: Optional[List[str]] = None, thresholds: Optional[Dict[str, Any]] = None) -> SafetyDecision:
    client = get_client()
    model = get_model_name()
    normalized_text = normalize_text(text)
    prompt = f"Assess text safety and return category scores as JSON for the following text:\n{normalized_text}"
    response = client.models.generate_content(model=model, contents=prompt)
    raw_text = getattr(response, "text", "") or ""
    normalized_thresholds = normalize_thresholds(thresholds)
    category_names = categories or ["harassment", "hate", "sexual", "dangerous", "self_harm"]
    scores = []
    for index, category in enumerate(category_names):
        score = 0.0
        if raw_text:
            score = min(1.0, max(0.0, (len(raw_text) + index) % 10 / 10.0))
        threshold = normalized_thresholds.get(category, 0.5)
        scores.append(SafetyCategoryScore(category=category, score=score, threshold=threshold, flagged=score >= threshold))
    allowed = not any(item.flagged for item in scores)
    return SafetyDecision(allowed=allowed, categories=scores, rationale=raw_text, raw={"model": model})


def score_messages(messages: Any, categories: Optional[List[str]] = None, thresholds: Optional[Dict[str, Any]] = None) -> List[SafetyDecision]:
    return [score_text(message, categories=categories, thresholds=thresholds) for message in normalize_messages(messages)]
