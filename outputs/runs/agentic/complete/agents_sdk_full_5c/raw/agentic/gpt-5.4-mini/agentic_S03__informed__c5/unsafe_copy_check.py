from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from translation_models import SafetyFinding


def check_unsafe_copy(texts: Iterable[str]) -> List[SafetyFinding]:
    client = OpenAI()
    findings: List[SafetyFinding] = []
    for text in texts:
        response = client.moderations.create(model="omni-moderation-latest", input=text)
        result = response.results[0]
        categories = {k: float(v) for k, v in result.categories.model_dump().items()}
        findings.append(SafetyFinding(text=text, score=float(result.category_scores.harassment), categories=categories))
    return findings
