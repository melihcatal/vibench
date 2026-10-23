from __future__ import annotations

from typing import Iterable, Sequence

from openai import OpenAI


MODEL_ID = "gpt-4o-mini"


def summarize_visual_analysis(labels: Sequence[str], text_blocks: Sequence[str], language: str = "en") -> str:
    client = OpenAI()
    prompt = (
        f"Summarize this visual analysis in {language} in one concise paragraph. "
        f"Labels: {', '.join(labels) or 'none'}. Text: {', '.join(text_blocks) or 'none'}."
    )
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
