from __future__ import annotations

import os

from openai import OpenAI

from speech_models import TranscriptResult, transcript_to_publishable_text


def archive_summary(result: TranscriptResult) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Create a concise archival summary for a batch speech transcription.",
            },
            {
                "role": "user",
                "content": transcript_to_publishable_text(result),
            },
        ],
        temperature=0.2,
    )
    return completion.choices[0].message.content or ""
