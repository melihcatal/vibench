from __future__ import annotations

import os
from collections.abc import Sequence

from openai import OpenAI

from speech_models import normalize_caption_chunk


def summarize_meeting_chunks(chunks: Sequence[str]) -> str:
    transcript = "\n".join(
        normalize_caption_chunk(chunk)
        for chunk in chunks
        if normalize_caption_chunk(chunk)
    )
    if not transcript:
        return ""
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize live meeting transcript chunks into concise action-oriented notes.",
            },
            {
                "role": "user",
                "content": transcript,
            },
        ],
    )
    return response.output_text.strip()
