import asyncio
import os
from typing import AsyncIterable

import openai

# OpenAI API credentials (environment variable)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

SUMMARY_MODEL = "gpt-4o-mini"  # suitable for short meeting chunks


async def summarize_chunks(chunks: AsyncIterable[str]) -> AsyncIterable[str]:
    """Summarizes each incoming transcript chunk using OpenAI GPT-4o-mini model."""
    prompt_template = (
        "Summarize the following meeting excerpt in 2-3 concise sentences:\n\n{}"
    )
    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model=SUMMARY_MODEL,
            messages=[{"role": "user", "content": prompt_template.format(chunk)}],
        )
        summary = response["choices"][0]["message"]["content"]
        yield summary


# Example integration with streaming transcript generator
# async for summary in summarize_chunks(stream_microphone_events):
#     print("Summary:", summary)
