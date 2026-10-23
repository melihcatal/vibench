import os
from typing import Iterable

from openai import OpenAI


def summarize_live_meeting_transcript(chunks: Iterable[str]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    transcript = "
".join(chunks)
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini"),
        messages=[
            {"role": "system", "content": "Summarize live meeting transcripts clearly and concisely."},
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content or ""
