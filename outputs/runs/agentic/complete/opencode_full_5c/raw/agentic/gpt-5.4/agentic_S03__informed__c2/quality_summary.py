from __future__ import annotations

import json
import os

from openai import OpenAI

from translation_models import QualitySummaryResult, compact_text


OPENAI_MODEL = os.getenv("OPENAI_QUALITY_MODEL", "gpt-4o-mini")
OPENAI_PROVIDER = "OpenAI"


def summarize_translation_quality(
    source_text: str, translated_text: str, target_language: str
) -> QualitySummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Review translation quality and return strict JSON with keys summary and issues.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            f"Target language: {target_language}\n"
                            f"Source: {source_text}\n"
                            f"Translation: {translated_text}"
                        ),
                    }
                ],
            },
        ],
        text={"format": {"type": "json_object"}},
    )
    payload = json.loads(response.output_text)
    issues = [
        compact_text(item) for item in payload.get("issues", []) if compact_text(item)
    ]
    return QualitySummaryResult(
        summary=compact_text(payload.get("summary")),
        issues=issues,
        provider=OPENAI_PROVIDER,
        model=OPENAI_MODEL,
        raw_response=response,
    )
