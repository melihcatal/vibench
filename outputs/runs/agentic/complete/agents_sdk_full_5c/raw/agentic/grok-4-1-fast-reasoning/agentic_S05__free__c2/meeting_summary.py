import asyncio
import os
from openai import AsyncOpenAI
from typing import AsyncGenerator

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def meeting_summary(transcript_chunks: AsyncGenerator[str, None]) -> AsyncGenerator[str, None]:
    context: list[str] = []
    async for chunk in transcript_chunks:
        context.append(chunk)
        context_text = " ".join(context)
        if len(context_text) > 2000:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Summarize the meeting transcript in bullet points."},
                    {"role": "user", "content": context_text}
                ]
            )
            summary = response.choices[0].message.content
            yield summary
            context = [summary]
    if context:
        context_text = " ".join(context)
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Provide final summary of the meeting."},
                {"role": "user", "content": context_text}
            ]
        )
        yield response.choices[0].message.content