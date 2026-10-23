import os
import asyncio
from openai import AsyncOpenAI
from typing import AsyncIterator
from speech_models import TranscriptChunk, TranscriptStream

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def summarize_meeting(
    stream: TranscriptStream, interval: int = 20
) -> AsyncIterator[str]:
    buffer = []
    count = 0
    async for chunk in stream:
        if chunk["is_final"]:
            buffer.append(chunk["transcript"])
            count += 1
            if count >= interval:
                full_text = " ".join(buffer)
                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": f"Summarize this meeting transcript: {full_text}",
                        }
                    ],
                )
                summary = response.choices[0].message.content
                yield summary
                buffer = []
                count = 0
    if buffer:
        full_text = " ".join(buffer)
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize this meeting transcript: {full_text}",
                }
            ],
        )
        yield response.choices[0].message.content
