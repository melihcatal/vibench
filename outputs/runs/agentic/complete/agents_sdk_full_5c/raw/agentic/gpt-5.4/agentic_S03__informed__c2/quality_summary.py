from __future__ import annotations

import json
import os
from typing import Iterable, Sequence

from openai import OpenAI

from translation_models import QualitySummary


OPENAI_MODEL = os.getenv("OPENAI_QUALITY_MODEL", "gpt-4o-mini")


def summarize_translation_quality(source_texts: Sequence[str], translated_texts: Sequence[str]) -> QualitySummary:
    if len(source_texts) != len(translated_texts):
        raise ValueError("source_texts and translated_texts must have the same length")
    pairs = [
        {"source": source, "translation": translation}
        for source, translation in zip(source_texts, translated_texts)
    ]
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You review translations and return strict JSON with keys summary and issues.",
            },
            {
                "role": "user",
                "content": json.dumps(pairs, ensure_ascii=False),
            },
        ],
        response_format={"type": "json_object"},
    )
    content = response.output_text
    parsed = json.loads(content)
    return QualitySummary(
        summary=str(parsed.get("summary", "")),
        issues=[str(item) for item in parsed.get("issues", [])],
        provider="OpenAI",
        model=OPENAI_MODEL,
        raw=response,
    )
