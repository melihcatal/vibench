from __future__ import annotations

from typing import Dict, Iterable

from openai import OpenAI


QUALITY_MODEL = "gpt-4o-mini"


def summarize_translation_quality(segments: Iterable[str]) -> Dict[str, str]:
    client = OpenAI()
    prompt = "Summarize translation quality issues for these segments:\n" + "\n".join(f"- {segment}" for segment in segments)
    completion = client.chat.completions.create(
        model=QUALITY_MODEL,
        messages=[
            {"role": "system", "content": "You analyze translation quality issues."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return {"provider": "openai", "model": QUALITY_MODEL, "summary": completion.choices[0].message.content or ""}
