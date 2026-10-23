import asyncio
from typing import AsyncGenerator, List
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def _sync_summarize(chunks: List[str]) -> str:
    context = ' '.join(chunks)
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'Provide a concise summary of the recent meeting transcript.'},
            {'role': 'user', 'content': context}
        ],
        max_tokens=200,
        temperature=0.3
    )
    return response.choices[0].message.content or ''

async def meeting_summary(transcript_stream: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
    buffer: List[str] = []
    loop = asyncio.get_running_loop()
    async for chunk in transcript_stream:
        buffer.append(chunk)
        buffer_size = sum(len(c) for c in buffer)
        if buffer_size > 1500:
            summary = await loop.run_in_executor(None, _sync_summarize, buffer)
            if summary:
                yield summary
            buffer = []
    if buffer:
        summary = await loop.run_in_executor(None, _sync_summarize, buffer)
        if summary:
            yield summary