from typing import Iterable

from openai import OpenAI

from speech_models import normalize_text


def summarize_meeting_transcript(chunks: Iterable[str]) -> str:
    client = OpenAI()
    text = "\n".join(normalize_text(chunk) for chunk in chunks if normalize_text(chunk))
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the meeting succinctly."},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content or ""
