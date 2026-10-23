from __future__ import annotations

import json
import os
from typing import Iterable, List

from openai import OpenAI

from speech_models import MeetingSummaryResult, join_caption_chunks


MODEL_NAME = "gpt-4o-mini"


def summarize_meeting_chunks(chunks: Iterable[str]) -> MeetingSummaryResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY for OpenAI chat completions")
    transcript = join_caption_chunks(chunks)
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You summarize meeting transcripts and extract action items as JSON with keys summary and action_items.",
            },
            {
                "role": "user",
                "content": transcript,
            },
        ],
    )
    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    action_items = data.get("action_items") or []
    if not isinstance(action_items, list):
        action_items = [str(action_items)]
    return MeetingSummaryResult(
        summary=str(data.get("summary", "")),
        action_items=[str(item) for item in action_items],
        raw={"provider": "OpenAI", "model": MODEL_NAME, "response_id": getattr(response, "id", None)},
    )
