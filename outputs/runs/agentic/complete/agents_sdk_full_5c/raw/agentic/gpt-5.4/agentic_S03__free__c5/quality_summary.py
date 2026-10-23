from __future__ import annotations

from translation_client import OPENAI_MODEL, get_openai_client
from translation_models import QualitySummaryResult


def summarize_translation_quality(
    source_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
) -> QualitySummaryResult:
    client = get_openai_client()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Summarize translation quality issues with focus on accuracy, fluency, terminology, omissions, and formatting. Return concise plain text.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Source ({source_language}): {source_text}\nTranslation ({target_language}): {translated_text}",
                    }
                ],
            },
        ],
    )
    summary = getattr(response, "output_text", "").strip()
    return QualitySummaryResult(
        summary=summary,
        provider="openai",
        raw=response.model_dump(),
    )
