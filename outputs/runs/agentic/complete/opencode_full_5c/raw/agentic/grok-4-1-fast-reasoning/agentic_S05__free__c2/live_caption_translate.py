import asyncio
import os
from openai import AsyncOpenAI
from typing import AsyncGenerator


async def translate_live_captions(
    caption_gen: AsyncGenerator[str, None], target_language: str = "es"
) -> AsyncGenerator[str, None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set")
    client = AsyncOpenAI(api_key=api_key)

    async for caption in caption_gen:
        if not caption.strip():
            continue
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"Translate English speech captions to {target_language} naturally.",
                },
                {"role": "user", "content": caption},
            ],
            max_tokens=200,
            temperature=0.1,
        )
        translated = response.choices[0].message.content.strip()
        yield translated
