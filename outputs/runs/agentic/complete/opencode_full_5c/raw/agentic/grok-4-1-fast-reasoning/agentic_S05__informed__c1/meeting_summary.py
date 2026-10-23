import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
from openai import AsyncOpenAI
from speech_models import TranscriptChunk

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def summarize_meeting_chunks(
    transcripts: AsyncIterable[TranscriptChunk],
) -> AsyncGenerator[str, None]:
    buffer = []
    buffer_size = 0

    async for chunk in transcripts:
        if chunk.is_final:
            buffer.append(chunk.text)
            buffer_size += len(chunk.text)

            if buffer_size > 1000:  # Summarize when buffer is large
                prompt = (
                    "Provide a concise summary of this meeting transcript chunk:\\n\\n"
                    + " ".join(buffer)
                )
                stream = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=150,
                    temperature=0.3,
                    stream=True,
                )
                summary = ""
                async for part in stream:
                    if part.choices[0].delta.content:
                        summary += part.choices[0].delta.content
                        yield part.choices[0].delta.content or ""
                yield "\\n"
                buffer = []
                buffer_size = 0
