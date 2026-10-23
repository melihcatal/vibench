from __future__ import annotations

import json
import os
from typing import Iterable, Optional

from openai import OpenAI

from translation_models import QualitySummaryResult

DEFAULT_MODEL = "gpt-4o-mini"


def quality_summary(
    source_text: str,
    translated_text: str,
    source_language: str,
    target_language: str,
    reviewer_notes: Optional[Iterable[str]] = None,
) -> QualitySummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    notes = list(reviewer_notes or [])
    prompt = {
        "task": "translation_quality_summary",
        "source_language": source_language,
        "target_language": target_language,
        "source_text": source_text,
        "translated_text": translated_text,
        "reviewer_notes": notes,
        "instructions": [
            "Summarize likely translation quality issues succinctly.",
            "Return JSON with keys: summary, issues.",
            "issues must be an array of short strings.",
        ],
    }
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_QUALITY_MODEL", DEFAULT_MODEL),
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a professional localization QA reviewer."},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
    )
    content = response.choices[0].message.content or "{}"
    payload = json.loads(content)
    issues = payload.get("issues") or []
    if not isinstance(issues, list):
        issues = [str(issues)]
    return QualitySummaryResult(
        summary=str(payload.get("summary", "")).strip(),
        issues=[str(item) for item in issues],
        provider="OpenAI",
        raw={
            "model": response.model,
            "usage": response.usage.model_dump() if response.usage else None,
        },
    )
