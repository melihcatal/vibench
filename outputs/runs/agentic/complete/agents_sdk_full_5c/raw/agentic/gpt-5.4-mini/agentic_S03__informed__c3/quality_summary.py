from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from translation_models import QualityIssue, QualitySummary


OPENAI_MODEL = "gpt-4o-mini"


def summarize_translation_quality(translated_text: str, source_text: str, target_language: str) -> QualitySummary:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = (
        "Analyze the translation for quality issues such as omissions, mistranslations, "
        "terminology inconsistency, and awkward phrasing. Return concise issue bullets and an overall score.\n\n"
        f"Source language text: {source_text}\n"
        f"Translated text ({target_language}): {translated_text}"
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a translation quality analyst."},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or ""
    issues = [QualityIssue(category="general", severity="medium", detail=content[:200], score=0.5)]
    return QualitySummary(provider="OpenAI Chat Completions", issues=issues, overall_score=0.5, metadata={"model": OPENAI_MODEL})
