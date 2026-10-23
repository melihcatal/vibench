import os

from openai import AsyncOpenAI

from speech_models import normalize_text


async def live_caption_translate(payload, config=None):
    config = config or {}
    client = AsyncOpenAI(api_key=config.get("openai_api_key") or os.getenv("OPENAI_API_KEY"))
    target_language = config.get("target_language") or payload.get("target_language") or "Spanish"
    async for chunk in payload["caption_chunks"]:
        text = normalize_text(chunk.get("text") if isinstance(chunk, dict) else chunk)
        if not text:
            continue
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Translate live captions into {target_language}."},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )
        yield {"text": response.choices[0].message.content, "source_text": text, "target_language": target_language}
