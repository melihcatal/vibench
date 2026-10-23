from __future__ import annotations

import os

from openai import OpenAI


def summarize_meeting_transcript(chunks: list[str]) -> dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI GPT-4o-mini")
    client = OpenAI(api_key=api_key)
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk.strip())
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "Summarize meeting transcript chunks into concise notes, decisions, and action items.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    summary = completion.choices[0].message.content or ""
    return {"summary": summary, "model": "gpt-4o-mini"}
