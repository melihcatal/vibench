from __future__ import annotations

import os
from collections.abc import Iterable

from openai import AsyncOpenAI


async def summarize_meeting_chunks(chunks: Iterable[str]) -> dict[str, str]:
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk.strip())
    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = await client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize meeting transcript chunks into concise action-oriented notes.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return {
        "summary": response.output_text,
        "provider": "OpenAI gpt-4.1-mini",
    }
