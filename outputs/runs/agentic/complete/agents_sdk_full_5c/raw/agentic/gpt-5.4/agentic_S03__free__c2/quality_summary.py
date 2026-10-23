from __future__ import annotations

from translation_client import OPENAI_PROVIDER, OPENAI_QUALITY_MODEL, build_quality_prompt, get_openai_client
from translation_models import QualitySummary


def quality_summary(source_text: str, translated_text: str, source_language: str, target_language: str) -> QualitySummary:
    client = get_openai_client()
    prompt = build_quality_prompt(source_text, translated_text, source_language, target_language)
    response = client.responses.create(
        model=OPENAI_QUALITY_MODEL,
        input=prompt,
    )
    text = response.output_text.strip()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    summary = lines[0] if lines else "No summary returned."
    issues = [line.lstrip("-• ") for line in lines[1:]]
    return QualitySummary(
        summary=summary,
        issues=issues,
        provider=OPENAI_PROVIDER,
        model=OPENAI_QUALITY_MODEL,
    )
