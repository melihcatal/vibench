import os
from typing import Iterable

from openai import OpenAI


def summarize_meeting(chunks: Iterable[str]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": "Summarize the meeting transcript succinctly.",
            },
            {"role": "user", "content": "\n".join(chunks)},
        ],
    )
    return response.choices[0].message.content or ""
