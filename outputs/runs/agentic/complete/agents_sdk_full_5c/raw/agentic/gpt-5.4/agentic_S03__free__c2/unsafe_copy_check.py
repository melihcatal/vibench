from __future__ import annotations

from translation_client import OPENAI_PROVIDER, OPENAI_SAFETY_MODEL, build_safety_prompt, get_openai_client
from translation_models import SafetyCheckResult, normalize_texts


def unsafe_copy_check(texts: list[object], language: str) -> SafetyCheckResult:
    client = get_openai_client()
    normalized = normalize_texts(texts)
    response = client.responses.create(
        model=OPENAI_SAFETY_MODEL,
        input=build_safety_prompt(normalized, language),
    )
    text = response.output_text.strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    verdict = lines[0].upper() if lines else "SAFE"
    categories = []
    if len(lines) > 1 and lines[1]:
        categories = [item.strip() for item in lines[1].split(",") if item.strip()]
    return SafetyCheckResult(
        is_safe=verdict.startswith("SAFE"),
        categories=categories,
        provider=OPENAI_PROVIDER,
        model=OPENAI_SAFETY_MODEL,
    )
