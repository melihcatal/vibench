import os
import asyncio
from typing import AsyncGenerator
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def summarize_live_meeting_chunks(chunks_gen: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
    transcript = ""
    word_count = 0
    async for chunk in chunks_gen:
        transcript += chunk + " "
        word_count += len(chunk.split())
        if word_count > 200:
            summary = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": f"Provide a concise summary of this live meeting transcript so far:\n\n{transcript}"}
                ],
                max_tokens=150,
            )
            yield summary.choices[0].message.content
            transcript = ""
            word_count = 0
    if transcript.strip():
        summary = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Summarize this meeting transcript:\n\n{transcript}"}
            ],
            max_tokens=150,
        )
        yield summary.choices[0].message.content
