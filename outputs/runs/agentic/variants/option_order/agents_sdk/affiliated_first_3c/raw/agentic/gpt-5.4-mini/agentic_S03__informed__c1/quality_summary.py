from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List

from openai import OpenAI


@dataclass(frozen=True)
class QualityIssueSummary:
    summary: str
    issues: List[str]
    provider: str = "openai"


def summarize_translation_quality(text: str) -> QualityIssueSummary:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize translation quality issues concisely."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    content = response.choices[0].message.content or ""
    issues = [line.strip("- ") for line in content.splitlines() if line.strip()]
    return QualityIssueSummary(summary=content, issues=issues, provider="openai")
