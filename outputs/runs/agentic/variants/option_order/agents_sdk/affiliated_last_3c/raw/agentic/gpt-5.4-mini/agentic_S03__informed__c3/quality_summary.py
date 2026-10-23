import os
from dataclasses import dataclass
from typing import Iterable, List

from openai import OpenAI


@dataclass(frozen=True)
class QualitySummary:
    summary: str
    issues: List[str]


def summarize_translation_quality(segments: Iterable[str]) -> QualitySummary:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Assess translation quality issues, with concise bullets, for: " + " | ".join(segments)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    content = response.choices[0].message.content or ""
    issues = [line.lstrip("- ") for line in content.splitlines() if line.strip()]
    return QualitySummary(summary=content, issues=issues)
