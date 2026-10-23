import os
import json
from typing import Iterable, List, Optional

from openai import OpenAI


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def summarize_meeting_chunks(chunks: Iterable[str], previous_summary: Optional[str] = None) -> str:
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk and chunk.strip())
    if not transcript:
        return previous_summary or ""

    client = OpenAI()

    messages = [
        {
            "role": "system",
            "content": "You summarize live meeting transcript chunks into concise, accurate meeting notes with decisions, action items, and open questions.",
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "previous_summary": previous_summary or "",
                    "new_transcript_chunks": transcript,
                    "instructions": [
                        "Update the running meeting summary based only on the provided transcript.",
                        "Preserve key decisions, action items, owners, deadlines, and open questions.",
                        "Keep the summary concise and avoid repetition.",
                    ],
                },
                ensure_ascii=False,
            ),
        },
    ]

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def summarize_live_transcript(stream_of_chunks: Iterable[str]) -> List[str]:
    summaries: List[str] = []
    running_summary: Optional[str] = None
    for chunk in stream_of_chunks:
        running_summary = summarize_meeting_chunks([chunk], running_summary)
        summaries.append(running_summary)
    return summaries
