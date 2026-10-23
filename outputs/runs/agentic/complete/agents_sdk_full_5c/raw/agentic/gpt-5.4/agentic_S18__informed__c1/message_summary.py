from __future__ import annotations

import os
from typing import Iterable, Mapping

from openai import OpenAI


MODEL = "gpt-4o-mini"
PROVIDER = "openai"


def summarize_results(results: Iterable[Mapping[str, object]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    rendered = "\n".join(f"- {dict(item)}" for item in results)
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Summarize pub/sub message processing outcomes for operations review."},
            {"role": "user", "content": f"Create a concise summary of these processing results:\n{rendered}"},
        ],
    )
    return response.choices[0].message.content or ""
