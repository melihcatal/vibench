from __future__ import annotations

import json
import os
from typing import Iterable, List, Optional

from openai import OpenAI

from translation_models import QualitySummaryResult


DEFAULT_MODEL = os.getenv("OPENAI_QUALITY_MODEL", "gpt-4o-mini")


def quality_summary(
    source_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
    reviewer_notes: Optional[Iterable[str]] = None,
) -> QualitySummaryResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    notes = list(reviewer_notes or [])
    prompt = {
        "task": "Summarize translation quality issues for a localized text.",
        "source_language": source_language,
        "target_language": target_language,
        "source_text": source_text,
        "translated_text": translated_text,
        "reviewer_notes": notes,
        "response_format": {
            "summary": "short paragraph",
            "issues": ["list of concise issue bullets"]
        },
    }
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a professional localization QA reviewer."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    )
    content = response.choices[0].message.content or "{}"
    parsed = json.loads(content)
    return QualitySummaryResult(
        summary=parsed.get("summary", ""),
        issues=[str(item) for item in parsed.get("issues", [])],
        provider="openai",
        model=DEFAULT_MODEL,
        raw=response,
    )
