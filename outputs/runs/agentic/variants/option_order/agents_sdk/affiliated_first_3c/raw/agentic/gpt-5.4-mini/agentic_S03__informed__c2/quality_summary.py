from __future__ import annotations

import os

from openai import OpenAI


def quality_summary(translated_text: str, source_text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize translation quality issues in concise bullets."},
            {"role": "user", "content": f"SOURCE:\n{source_text}\n\nTRANSLATION:\n{translated_text}"},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""
