import os

from openai import AsyncOpenAI

from speech_models import normalize_text


async def live_caption_safety(payload, config=None):
    config = config or {}
    client = AsyncOpenAI(api_key=config.get("openai_api_key") or os.getenv("OPENAI_API_KEY"))
    policy = config.get("policy") or "Flag unsafe, hateful, harassing, sexual, or violent content."
    async for chunk in payload["caption_chunks"]:
        text = normalize_text(chunk.get("text") if isinstance(chunk, dict) else chunk)
        if not text:
            continue
        response = await client.moderations.create(model="omni-moderation-latest", input=text)
        result = response.results[0]
        yield {"text": text, "unsafe": bool(result.flagged), "categories": dict(result.categories), "policy": policy}
