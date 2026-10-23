from __future__ import annotations

from dataclasses import asdict
from typing import List

from openai import OpenAI

from translation_models import QualitySummary

PROVIDER = "openai"
MODEL = "gpt-4.1-mini"


def summarize_translation_quality(translated_text: str) -> QualitySummary:
    client = OpenAI()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Summarize likely translation quality issues in concise bullet points."},
            {"role": "user", "content": translated_text},
        ],
        temperature=0,
    )
    issues_text = response.choices[0].message.content or ""
    issues = [line.strip("- •\t ") for line in issues_text.splitlines() if line.strip()]
    return QualitySummary(translated_text=translated_text, issue_count=len(issues), issues=issues, provider=PROVIDER)
