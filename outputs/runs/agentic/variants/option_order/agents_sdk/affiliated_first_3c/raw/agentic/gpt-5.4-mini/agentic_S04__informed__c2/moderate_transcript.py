from __future__ import annotations

from openai import OpenAI


CONTENT_SAFETY_MODEL = "gpt-4o-mini"


def moderate_transcript(text: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model=CONTENT_SAFETY_MODEL,
        messages=[
            {"role": "system", "content": "Classify whether transcript text is safe for publication. Return a concise moderation note."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return response.choices[0].message.content or ""
