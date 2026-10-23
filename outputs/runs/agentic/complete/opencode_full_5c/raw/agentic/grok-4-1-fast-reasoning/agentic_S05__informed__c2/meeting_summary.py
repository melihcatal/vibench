import asyncio
from typing import AsyncGenerator
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def summarize_meeting_chunks(
    transcript_stream: AsyncGenerator[str, None],
) -> AsyncGenerator[str, None]:
    async for chunk in transcript_stream:
        if not chunk.strip():
            continue
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a concise meeting note taker."},
                {
                    "role": "user",
                    "content": f"Summarize this meeting transcript chunk:\n\n{chunk}",
                },
            ],
            max_tokens=150,
        )
        yield response.choices[0].message.content
