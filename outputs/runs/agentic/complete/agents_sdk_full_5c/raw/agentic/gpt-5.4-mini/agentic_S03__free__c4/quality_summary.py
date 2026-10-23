"""Summarize translation quality issues using OpenAI."""

from __future__ import annotations

import os
from typing import List

from openai import OpenAI

OPENAI_MODEL = "gpt-4o-mini"


def summarize_quality_issues(translated_text: str, source_text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        "Summarize translation quality issues in concise bullets. "
        "Compare source and translated text, mention omissions, tone shifts, terminology drift, and awkward phrasing."
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"SOURCE:\n{source_text}\n\nTRANSLATION:\n{translated_text}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


__all__ = ["summarize_quality_issues", "OPENAI_MODEL"]
