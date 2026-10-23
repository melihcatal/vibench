from __future__ import annotations

from typing import Iterable

from openai import OpenAI

from speech_models import CaptionSegment, merge_caption_segments


def summarize_meeting_chunks(chunks: Iterable[CaptionSegment]) -> str:
    transcript = merge_caption_segments(chunks)
    client = OpenAI(api_key=None)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize meeting transcript chunks into concise action-oriented notes.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return response.output_text
