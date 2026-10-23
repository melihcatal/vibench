import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
from openai import AsyncOpenAI

async def meeting_summary(
    transcript_chunks: AsyncIterable[str],
    max_buffer_size: int = 3000
) -> AsyncGenerator[str, None]:
    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    buffer = ''
    async for chunk in transcript_chunks:
        buffer += ' ' + chunk
        if len(buffer) &gt; max_buffer_size:
            response = await client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {
                        'role': 'system',
                        'content': 'Summarize meeting transcripts concisely, focusing on key points, decisions, and action items.'
                    },
                    {'role': 'user', 'content': buffer.strip()}
                ],
                max_tokens=200,
                temperature=0.3
            )
            yield response.choices[0].message.content
            buffer = ''
    if buffer.strip():
        response = await client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    'role': 'system',
                    'content': 'Summarize meeting transcripts concisely, focusing on key points, decisions, and action items.'
                },
                {'role': 'user', 'content': buffer.strip()}
            ],
            max_tokens=200,
            temperature=0.3
        )
        yield response.choices[0].message.content