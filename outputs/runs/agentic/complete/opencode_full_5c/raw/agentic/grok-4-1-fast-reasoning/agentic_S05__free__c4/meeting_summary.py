import asyncio
from typing import AsyncGenerator
from openai import AsyncOpenAI
import os

async def summarize_meeting_chunks(chunks: AsyncGenerator[str, None], model: str = &quot;gpt-4o-mini&quot;) -> AsyncGenerator[str, None]:
    api_key = os.getenv(&quot;OPENAI_API_KEY&quot;)
    if not api_key:
        raise ValueError(&quot;OPENAI_API_KEY environment variable is required&quot;)
    client = AsyncOpenAI(api_key=api_key)
    buffer = []
    async for chunk in chunks:
        buffer.append(chunk)
        buffered_text = &quot; &quot;.join(buffer)
        if len(buffered_text) &gt; 500:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {&quot;role&quot;: &quot;system&quot;, &quot;content&quot;: &quot;Provide concise bullet summaries for meeting transcripts.&quot;},
                    {&quot;role&quot;: &quot;user&quot;, &quot;content&quot;: buffered_text}
                ],
                max_tokens=200,
            )
            summary = response.choices[0].message.content.strip()
            yield summary
            buffer = []
        else:
            yield chunk
