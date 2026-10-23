import asyncio
import os
from typing import AsyncGenerator, AsyncIterable, List
import openai
from speech_models import Transcript


async def meeting_summary(
    caption_stream: AsyncIterable[Transcript],
    model: str = "gpt-4o-mini",
    api_key: str | None = None,
) -> AsyncGenerator[str, None]:
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    client = openai.AsyncOpenAI(api_key=api_key)
    buffer: List[str] = []
    async for transcript in caption_stream:
        if transcript["is_final"]:
            text = transcript["text"].strip()
            if text:
                buffer.append(text)
                buffered_text = " ".join(buffer)
                if len(buffered_text) > 500:
                    prompt = f"Summarize the following meeting discussion concisely:\\n{buffered_text}\\n\\nSummary:"
                    response = await client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=150,
                    )
                    summary = response.choices[0].message.content or ""
                    yield summary
                    buffer = []
    if buffer:
        buffered_text = " ".join(buffer)
        prompt = f"Summarize the following meeting discussion concisely:\\n{buffered_text}\\n\\nSummary:"
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        yield response.choices[0].message.content or ""
