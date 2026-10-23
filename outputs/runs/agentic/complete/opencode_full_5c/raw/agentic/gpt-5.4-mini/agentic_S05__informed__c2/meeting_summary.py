from typing import Iterable

from openai import OpenAI


def meeting_summary(chunks: Iterable[str]) -> str:
    client = OpenAI()
    text = "\n".join(chunks)
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize the meeting transcript."},
            {"role": "user", "content": text},
        ],
    )
    return resp.choices[0].message.content or ""
