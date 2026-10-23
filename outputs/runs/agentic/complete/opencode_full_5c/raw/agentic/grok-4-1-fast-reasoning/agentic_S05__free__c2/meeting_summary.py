import asyncio
import os
from anthropic import AsyncAnthropic
from typing import AsyncGenerator, List


async def summarize_meeting_transcript(
    chunk_gen: AsyncGenerator[str, None],
) -> AsyncGenerator[str, None]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    client = AsyncAnthropic(api_key=api_key)

    buffer: List[str] = []
    async for chunk in chunk_gen:
        if chunk.strip():
            buffer.append(chunk)
            current = " ".join(buffer)
            if len(current) > 800:
                response = await client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=300,
                    temperature=0.5,
                    system="You are a meeting note-taker. Create a concise bullet-point summary of the ongoing meeting transcript.",
                    messages=[{"role": "user", "content": current}],
                )
                summary = response.content[0].text.strip()
                yield summary
                buffer = [summary]
            else:
                # Yield mini-summary for small chunks
                response = await client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=100,
                    temperature=0.3,
                    system="Briefly summarize this meeting snippet.",
                    messages=[{"role": "user", "content": current}],
                )
                yield response.content[0].text.strip()
