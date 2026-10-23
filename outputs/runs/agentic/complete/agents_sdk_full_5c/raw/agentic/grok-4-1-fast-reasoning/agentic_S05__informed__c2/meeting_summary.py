import asyncio
import os
from anthropic import Anthropic
from typing import AsyncGenerator, AsyncIterable

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

async def meeting_summary(transcripts: AsyncIterable[str]) -> AsyncGenerator[str, None]:
    buffer = ""
    async for chunk in transcripts:
        buffer += " " + chunk
        if len(buffer) > 800:
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=250,
                system="Provide a concise running summary of the meeting transcript.",
                messages=[{"role": "user", "content": buffer}]
            )
            summary = message.content[0].text
            yield summary
            buffer = summary