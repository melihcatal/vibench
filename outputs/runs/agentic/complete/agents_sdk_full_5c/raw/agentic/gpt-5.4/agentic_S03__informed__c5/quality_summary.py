from __future__ import annotations

import json
import os
from typing import Iterable, List, Sequence

from openai import OpenAI

from translation_models import QualityIssueSummary


OPENAI_MODEL = os.getenv("OPENAI_QUALITY_MODEL", "gpt-4o-mini")


def summarize_translation_quality(
    source_texts: Sequence[str],
    translated_texts: Sequence[str],
    target_language: str,
) -> QualityIssueSummary:
    if len(source_texts) != len(translated_texts):
        raise ValueError("source_texts and translated_texts must have the same length.")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    paired: List[dict] = [
        {"source": src, "translation": dst}
        for src, dst in zip(source_texts, translated_texts)
    ]
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You review translations for fluency, accuracy, terminology, omissions, and formatting. "
                    "Return JSON with keys summary and issues. issues must be an array of short strings."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "target_language": target_language,
                        "pairs": paired,
                    },
                    ensure_ascii=False,
                ),
            },
        ],
    )
    content = response.choices[0].message.content or "{}"
    parsed = json.loads(content)
    return QualityIssueSummary(
        summary=str(parsed.get("summary", "")),
        issues=[str(item) for item in parsed.get("issues", [])],
        provider="OpenAI",
        model=OPENAI_MODEL,
    )
