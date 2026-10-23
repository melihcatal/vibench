import asyncio
import os
from openai import AsyncOpenAI
from typing import AsyncGenerator

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

async def summarize_meeting_transcript(
    transcript_chunks
) -> AsyncGenerator[str, None]:
    if not OPENAI_API_KEY:
        raise ValueError('OPENAI_API_KEY environment variable is required.')
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    messages = [
        {
            "role": "system",
            "content": "You are an assistant that generates concise running summaries of live meeting transcripts. Respond only with the updated summary."
        }
    ]
    async for chunk in transcript_chunks:
        if chunk.strip():
            messages.append({"role": "user", "content": chunk})
            stream = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                stream=True,
                temperature=0.3
            )
            delta_summary = ""
            async for part in stream:
                if part.choices[0].delta.content:
                    content = part.choices[0].delta.content
                    delta_summary += content
                    yield content
            if delta_summary:
                messages.append({"role": "assistant", "content": delta_summary})
