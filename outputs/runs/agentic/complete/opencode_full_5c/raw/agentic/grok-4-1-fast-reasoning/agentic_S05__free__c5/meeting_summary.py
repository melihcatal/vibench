import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
from openai import AsyncOpenAI


async def summarize_meeting_transcript(
    transcript_iter: AsyncIterable[str],
) -> AsyncGenerator[str, None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = AsyncOpenAI(api_key=api_key)
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes meetings. Respond with concise bullet points of key discussion points, decisions, and action items.",
        }
    ]
    buffer = ""
    async for chunk in transcript_iter:
        buffer += " " + chunk
        if len(buffer) > 2000:
            messages.append({"role": "user", "content": buffer})
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=300,
            )
            summary = response.choices[0].message.content
            yield summary
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meetings. Respond with concise bullet points of key discussion points, decisions, and action items.",
                },
                {"role": "assistant", "content": summary},
            ]
            buffer = ""
    if buffer.strip():
        messages.append({"role": "user", "content": buffer})
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
        )
        yield response.choices[0].message.content
