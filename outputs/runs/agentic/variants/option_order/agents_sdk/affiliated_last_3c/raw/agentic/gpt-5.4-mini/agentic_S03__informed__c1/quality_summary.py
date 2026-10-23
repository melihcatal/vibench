from __future__ import annotations

import os
from typing import Iterable, List

from openai import OpenAI

from translation_models import QualitySummary, normalize_text_list, score_issues

PROVIDER_NAME = "OpenAI"
MODEL_ID = "gpt-4o-mini"


def summarize_translation_quality(segments: Iterable[str]) -> QualitySummary:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    normalized = normalize_text_list(segments)
    prompt = "Assess translation quality issues for these segments and return a concise JSON-style list of issues: " + " | ".join(normalized)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": "You summarize translation quality issues."},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or ""
    issues: List[str] = [line.strip("-• \t") for line in content.splitlines() if line.strip()]
    return QualitySummary(provider=PROVIDER_NAME, issues=issues, score=score_issues(issues))
