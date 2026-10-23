from openai import OpenAI
from typing import AsyncIterable

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def translate_text(text: str, target_language: str = "es") -> str:
    """Translates live captions into another language using OpenAI's GPT model."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"Translate the following text to {target_language}. Only return the translated text.",
            },
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


async def live_caption_translate(captions: AsyncIterable[str]):
    """Translates live captions into another language."""
    async for caption in captions:
        translated = await translate_text(caption)
        yield translated
