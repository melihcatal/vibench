from __future__ import annotations

import json
from typing import Iterable, List

from translation_client import OPENAI_MODEL, openai_client
from translation_models import QualitySummary


def quality_summary(source_texts: Iterable[str], translated_texts: Iterable[str], target_language: str) -> QualitySummary:
    pairs: List[dict] = []
    for source, translated in zip(source_texts, translated_texts):
        pairs.append({"source": source, "translation": translated})
    prompt = (
        "Review translation quality for the target language and return JSON with keys "
        "summary and issues. Focus on mistranslation, omission, tone, terminology, and fluency.\n"
        f"Target language: {target_language}\n"
        f"Pairs: {json.dumps(pairs, ensure_ascii=False)}"
    )
    response = openai_client().responses.create(
        model=OPENAI_MODEL,
        input=prompt,
        temperature=0,
    )
    text = response.output_text
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = {"summary": text.strip(), "issues": []}
    return QualitySummary(summary=str(data.get("summary", "")), issues=[str(x) for x in data.get("issues", [])], raw=response.model_dump())
