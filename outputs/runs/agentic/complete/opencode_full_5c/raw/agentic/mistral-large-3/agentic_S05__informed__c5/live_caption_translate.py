import os
from typing import AsyncGenerator, Dict, Any
from openai import AsyncOpenAI


async def live_caption_translate(
    transcript_stream: AsyncGenerator[Dict[str, Any], None],
    target_language: str = "es",
) -> AsyncGenerator[Dict[str, Any], None]:
    """Translates live captions into another language using OpenAI's GPT model."""
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    async for transcript in transcript_stream:
        text = transcript["transcript"]
        is_final = transcript["is_final"]

        if not text.strip():
            continue

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"Translate the following text to {target_language}.",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.3,
        )
        translated_text = response.choices[0].message.content.strip()
        yield {
            "original": text,
            "translated": translated_text,
            "is_final": is_final,
            "target_language": target_language,
        }
