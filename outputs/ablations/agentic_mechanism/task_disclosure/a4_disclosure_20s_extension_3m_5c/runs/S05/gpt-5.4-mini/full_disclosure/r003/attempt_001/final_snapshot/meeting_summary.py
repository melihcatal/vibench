import os
from typing import Iterable, List

from openai import OpenAI


def summarize_meeting_transcript(chunks: Iterable[str]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk and chunk.strip())
    if not transcript:
        return ""
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize live meeting transcript chunks into a concise, factual meeting summary with key decisions, action items, and open questions.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content or ""


def summarize_meeting_transcript_chunks(chunks: List[str]) -> str:
    return summarize_meeting_transcript(chunks)
