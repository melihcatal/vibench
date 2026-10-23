from __future__ import annotations

import os
from typing import Iterable

from openai import OpenAI

from speech_models import SummaryResult, merge_segments


OPENAI_MEETING_MODEL = "gpt-4o-mini"



def summarize_meeting_chunks(chunks: Iterable[str]) -> SummaryResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    transcript = merge_segments(type("Seg", (), {"text": chunk})() for chunk in chunks)
    response = client.chat.completions.create(
        model=OPENAI_MEETING_MODEL,
        messages=[
            {"role": "system", "content": "Summarize the meeting transcript into concise action items and decisions."},
            {"role": "user", "content": transcript},
        ],
        temperature=0.2,
    )
    return SummaryResult(summary=response.choices[0].message.content or "", model=OPENAI_MEETING_MODEL)
