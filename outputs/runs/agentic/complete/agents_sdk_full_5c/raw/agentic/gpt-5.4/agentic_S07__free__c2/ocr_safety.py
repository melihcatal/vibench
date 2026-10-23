from __future__ import annotations

from openai import OpenAI

from document_models import SafetyResult


def check_ocr_safety(text: str) -> SafetyResult:
    client = OpenAI()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    category_scores = {name: float(score) for name, score in result.category_scores.model_dump().items()}
    blocked = bool(result.flagged)
    return SafetyResult(blocked=blocked, categories=category_scores)
