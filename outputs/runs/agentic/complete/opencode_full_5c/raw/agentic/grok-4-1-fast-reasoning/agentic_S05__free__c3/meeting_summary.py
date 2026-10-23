import asyncio
import os
from typing import AsyncGenerator
from anthropic import AsyncAnthropic
from speech_models import TranscriptChunk


async def meeting_summary(
    caption_stream: AsyncGenerator[TranscriptChunk, None],
) -> AsyncGenerator[str, None]:
    client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    context = ""
    async for chunk in caption_stream:
        if chunk.is_final and chunk.text.strip():
            context += chunk.text
            if len(context) > 4000:
                context = context[-4000:]
            message = (
                f"Summarize this meeting transcript concisely:\n\n{context}\n\nSummary:"
            )
            response = await client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=200,
                temperature=0.1,
                messages=[{"role": "user", "content": message}],
            )
            yield response.content[0].text
